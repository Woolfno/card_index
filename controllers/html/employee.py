from typing import Annotated
from uuid import UUID

from litestar import get, post
from litestar.controller import Controller
from litestar.enums import RequestEncodingType
from litestar.exceptions import NotFoundException
from litestar.params import Body
from litestar.response import Redirect, Template

from models.models import Employee, Position
from schemas.employee import EmployeeIn, EmployeeWithPhoto
from services.employee import EmployeeService


class EmployeeController(Controller):
    include_in_schema = True
    path = "/employee"

    @get("/create")
    async def create_form(self)->Template:        
        positions = await Position.all()
        employees = await Employee.all()
        return Template(template_name="employee/create.html", 
                        context={"positions": positions, "bosses":employees})
    
    @post("/create")
    async def create(self,
                     data:Annotated[EmployeeWithPhoto, Body(media_type=RequestEncodingType.MULTI_PART)])->Redirect:        
        employe_in = EmployeeIn(**data.model_dump(exclude="photo_file"))        
        e = await EmployeeService.create(employe_in, data.photo_file)
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
        employee_in = EmployeeIn(**data.model_dump(exclude="photo_file"))
        photo_file = data.photo_file
        e = await EmployeeService.update(id, employee_in, photo_file)
        if e is None:
            raise NotFoundException
        return Redirect(f"/employee/{e.id}")
    
    @get("/{id:uuid}")
    async def get_employee(self, id:UUID)->Template:
        e = await EmployeeService.get_by_id(id)
        if e is None:
            raise NotFoundException
        return Template(template_name="employee/card.html", 
                        context={"employee":e})
    
    @get("/delete/{id:uuid}")
    async def delete_employee(self, id:UUID)->Redirect:
        if await EmployeeService.remove(id):
            return Redirect("/tree")
        return Redirect('/tree')
    