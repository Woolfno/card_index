from datetime import datetime
from pathlib import Path
from uuid import UUID

import aiofiles
from litestar.datastructures import UploadFile
from tortoise.transactions import in_transaction
from tortoise.exceptions import OperationalError
from litestar.exceptions import InternalServerException
from models.models import Employee
from schemas.employee import EmployeeIn
from settings import settings


class EmployeeService:
    # path to save on db and view in html page
    @staticmethod
    def _get_fileurl(filename:str)->str:
        return Path(settings.MEDIA_URL) / filename
    
    # path to save on disk
    @staticmethod
    def _get_filepath(filename:str)->str:
        return Path(settings.MEDIA_ROOT) / filename
    
    @staticmethod 
    def _generate_filename(filename:str)->str:
        name, ext = filename.split('.')
        return f"{datetime.now().strftime("%d%m%Y%H%M%S")}_{name}.{ext}"
    
    @staticmethod
    async def _save_file(src:UploadFile, dst:str):
        async with aiofiles.open(dst, "wb") as out:
            while content:=await src.read(1024):
                await out.write(content)          

    @staticmethod
    async def get_by_id(id:UUID)->Employee:
        return await Employee.get_or_none(id=id).prefetch_related("position", "boss")

    @staticmethod
    async def create(employee:EmployeeIn, photo_file:UploadFile|None)->Employee:
        if photo_file is not None:
            filename = EmployeeService._generate_filename(photo_file.filename)
            e = await Employee.create(**employee.model_dump(exclude_none=True, exclude_unset=True),
                                    photo_url=EmployeeService._get_fileurl(filename))
            filepath = EmployeeService._get_filepath(filename)
            await EmployeeService._save_file(photo_file, filepath)
        else:
            e = await Employee.create(**employee.model_dump(exclude_none=True, exclude_unset=True))
        return e
    
    @staticmethod
    async def update(id:UUID, employee:EmployeeIn, photo_file:UploadFile|None)->Employee:
        try:
            async with in_transaction() as connection:
                e = await Employee.get_or_none(id=id, using_db=connection)             
                if e is None:
                    return None
                if photo_file is not None:
                    filename = EmployeeService._generate_filename(photo_file.filename)
                    filepath = EmployeeService._get_filepath(filename)
                    await EmployeeService._save_file(photo_file, filepath)
                    await Employee.filter(id=id).using_db(connection).update(
                        **employee.model_dump(exclude_unset=True, exclude_none=False), 
                        photo_url=EmployeeService._get_fileurl(filename),
                        )
                else:
                    await Employee.filter(id=id).using_db(connection).update(
                        **employee.model_dump(exclude_unset=True, exclude_none=False),
                        )                    
        except OperationalError:
            raise InternalServerException
        return e
    
    @staticmethod
    async def remove(id:UUID)->bool:
        async with in_transaction() as connection:
            emp = await Employee.get_or_none(id=id, using_db=connection)
            if emp is None:
                return False            
            await emp.delete(using_db=connection)
            return True
