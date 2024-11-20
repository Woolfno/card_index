from pathlib import Path
from typing import Annotated
from uuid import UUID

import aiofiles
from datetime import datetime
from litestar import get, post
from litestar.controller import Controller
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import InternalServerException, NotFoundException
from litestar.params import Body
from litestar.response import Redirect, Template
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction

from models.models import Employee, Position
from schemas.employee import EmployeeWithPhoto
from settings import settings


class EmployeeController(Controller):
    include_in_schema = True
    path = "/employee"

    @get("/create")
    async def create_form(self)->Template:        
        positions = await Position.all()
        employees = await Employee.all()
        return Template(template_name="employee/create.html", 
                        context={"positions": positions, "bosses":employees})
    
    async def _save_file(self, src:UploadFile, dst:str):
        async with aiofiles.open(dst, "wb") as out:
            while content:=await src.read(1024):
                await out.write(content)      
    
    # path to save on db and view in html page
    def _get_fileurl(self, filename:str)->str:
        return Path(settings.MEDIA_URL) / filename
    
    # path to save on disk
    def _get_filepath(self, filename:str)->str:
        return Path(settings.MEDIA_ROOT) / filename
            
    def _generate_filename(self, filename:str)->str:
        name, ext = filename.split('.')
        return f"{datetime.now().strftime("%d%m%Y%H%M%S")}_{name}.{ext}"

    @post("/create")
    async def create(self,
                     data:Annotated[EmployeeWithPhoto, Body(media_type=RequestEncodingType.MULTI_PART)])->Redirect:
        filename = self._generate_filename(data.photo_file.filename)
        e = await Employee.create(**data.model_dump(exclude_none=True, exclude_unset=True),
                                  photo_url=self._get_fileurl(filename))
        filepath = self._get_filepath(filename)
        await self._save_file(data.photo_file, filepath)
        return Redirect(path=f"/employee/{e.id}") 
    
    @get("/edit/{id:uuid}")
    async def update_form(self, id:UUID)->Template:
        e = await Employee.get_or_none(id=id)
        if e is None:
            raise NotFoundException
        positions = await Position.all()
        employees = await Employee.all()
        return Template(template_name="employee/edit.html", 
                        context={"employee":e, "positions": positions, "bosses":employees})

    @post("/edit/{id:uuid}")
    async def update(self, 
                     data:Annotated[EmployeeWithPhoto, Body(media_type=RequestEncodingType.MULTI_PART)], 
                     id:UUID)->Redirect:        
        try:
            async with in_transaction() as connection:
                e = await Employee.get_or_none(id=id, using_db=connection)             
                if e is None:
                    raise NotFoundException
                if data.photo_file is not None:
                    filename = self._generate_filename(data.photo_file.filename)
                    filepath = self._get_filepath(filename)
                    await self._save_file(data.photo_file, filepath)
                    await Employee.filter(id=id).using_db(connection).update(
                        **data.model_dump(exclude_unset=True, exclude_none=True, exclude="photo_file"), 
                        photo_url=self._get_fileurl(filename),
                        )
                else:
                    await Employee.filter(id=id).using_db(connection).update(
                        **data.model_dump(exclude_unset=True, exclude_none=True),
                        )                    
        except OperationalError:
            raise InternalServerException
        return Redirect(f"/employee/{id}")
    
    @get("/{id:uuid}")
    async def get_employee(self, id:UUID)->Template:
        e = await Employee.get_or_none(id=id).prefetch_related("position", "boss")
        if e is None:
            raise NotFoundException
        return Template(template_name="employee/card.html", 
                        context={"employee":e})
    
    @get("/delete/{id:uuid}")
    async def delete_employee(self, id:UUID)->Redirect:
        async with in_transaction() as connection:
            e = await Employee.get_or_none(id=id, using_db=connection)
            if e is None:
                return Redirect("/tree")
            await e.delete(using_db=connection)
            return Redirect("/tree")
    