from typing import Any
import uuid
from pprint import pprint
from litestar import Controller, delete, get, patch, post, Request
from litestar.exceptions import HTTPException
from litestar.pagination import OffsetPagination
from litestar.status_codes import HTTP_404_NOT_FOUND
from litestar.security.jwt.token import Token
from pydantic import TypeAdapter

from models import models
from schemas import employee
from schemas.user import UserPydantic as User


async def get_employee(emp:models.Employee)->models.Employee:
    emp.position = await models.Position.get_or_none(id=emp.position_id)
    emp.boss = await models.Employee.get_or_none(id=emp.boss_id).prefetch_related('position')    
    if emp.boss is None:
        return emp
    emp.boss = await get_employee(emp.boss)
    return emp


class EmployeeController(Controller):
    path = "/employee"

    @get("/")
    async def list(self, limit:int=-1, offset:int=0)->OffsetPagination[employee.EmployeeAll]:
        total = await models.Employee.all().count()
        lst = await models.Employee.all().prefetch_related('position')
        ta = TypeAdapter(list[employee.EmployeeAll])
        return OffsetPagination[employee.EmployeeAll](
            items=ta.validate_python(lst, from_attributes=True),
            total=total,
            limit=limit,
            offset=offset,
        )
    
    @get("/{id:uuid}")
    async def get_by_id(self, id:uuid.UUID)->employee.Employee:       
        emp = await  models.Employee.get_or_none(id=id).prefetch_related('position', 'boss')
        if emp is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)
        if emp.boss is not None:
            emp.boss = await get_employee(emp.boss)
        return employee.Employee.model_validate(emp)
    
    @post()
    async def create(self, data:employee.EmployeeIn)->employee.Employee:
        empl = await models.Employee.create(**data.model_dump(exclude_unset=True, exclude_none=True))
        return employee.Employee.model_validate(empl)
    
    @patch("/{id:uuid}")
    async def update(self, id:uuid.UUID, data:employee.EmployeeIn)->employee.Employee:
        emp = await models.Employee.update_from_dict(data.model_dump(exclude_none=True, exclude_unset=True))
        return employee.Employee.model_validate(emp)

    @delete("/{id:uuid}")
    async def remove(self, id: uuid.UUID)->None:
        await models.Employee.filter(id=id).delete()