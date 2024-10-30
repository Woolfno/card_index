import uuid

from litestar import Controller, delete, get, post
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_404_NOT_FOUND

from db import db
from models import models


class EmployeeController(Controller):
    path = "/"

    @get("/")
    async def list(self)->models.Employee:
        return db.employes
    
    @get("/{id:uuid}")
    async def get_by_id(self, id:uuid.UUID)->models.Employee:
        for emp in db.employes:
            if id==emp.id:
                return emp
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    
    @post()
    async def create(self, data:db.Employee)->models.Employee:
        empl = await models.Employee.create(data)
        return db.Employee.model_validate(empl)
    
    @delete("/{id:uuid}")
    async def remove(self, id: uuid.UUID)->None:
        for emp in db.employes:
            if emp.id==id:
                db.employes.remove(emp)