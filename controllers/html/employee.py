from typing import Annotated
from uuid import UUID

from litestar import get, post
from litestar.controller import Controller
from litestar.enums import RequestEncodingType
from litestar.exceptions import NotFoundException, InternalServerException
from litestar.params import Body
from litestar.response import Redirect, Template
from tortoise.transactions import in_transaction
from tortoise.exceptions import OperationalError

from models.models import Employee, Position
from schemas.employee import EmployeeIn


class EmployeeController(Controller):
    include_in_schema = True
    path = "/employee"

    @get("/create")
    async def create_form(self)->Template:        
        positions = await Position.all()
        employees = await Employee.all()
        return Template(template_name="employee/create.html", context={"positions": positions, "bosses":employees})

    @post("/create")
    async def create(self, data:Annotated[EmployeeIn, Body(media_type=RequestEncodingType.URL_ENCODED)])->Redirect:
        e = await Employee.create(**data.model_dump(exclude_none=True, exclude_unset=True))
        return Redirect(path=f"/employee/{e.uuid}")
    
    @get("/edit/{id:uuid}")
    async def update_form(self, id:UUID)->Template:
        e = await Employee.get_or_none(uuid=id)
        if e is None:
            raise NotFoundException
        positions = await Position.all()
        employees = await Employee.all()
        return Template(template_name="employee/edit.html", 
                        context={"employee":e, "positions": positions, "bosses":employees})

    @post("/edit/{id:uuid}")
    async def update(self,data:Annotated[EmployeeIn, Body(media_type=RequestEncodingType.URL_ENCODED)], id:UUID)->Redirect:
        try:
            async with in_transaction() as connection:
                e = await Employee.get_or_none(uuid=id, using_db=connection)                    
                if e is None:
                    raise NotFoundException
                await Employee.filter(uuid=id).using_db(connection).update(**data.model_dump(exclude_unset=True, exclude_none=True))
        except OperationalError:
            raise InternalServerException
        return Redirect(f"/employee/{id}")
    
    @get("/{id:uuid}")
    async def get_employee(self, id:UUID)->Template:
        e = await Employee.get_or_none(uuid=id).prefetch_related("position", "boss")
        if e is None:
            raise NotFoundException
        return Template(template_name="employee/card.html", context={"employee":e})
    
    @get("/delete/{id:uuid}")
    async def delete_employee(self, id:UUID)->Redirect:
        e = await Employee.get_or_none(uuid=id)
        if e is None:
            return Redirect("/table")
        await e.delete()
        return Redirect("/table")
    