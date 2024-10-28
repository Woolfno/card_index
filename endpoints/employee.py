from model import model
from db import db
import uuid
from litestar import Controller, get, post, delete
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_404_NOT_FOUND


class EmployeeController(Controller):
    path = "/"

    @get("/")
    async def list(self)->model.Employee:
        return db.employes
    
    @get("/{id:uuid}")
    async def get_by_id(self, id:uuid.UUID)->model.Employee:
        for emp in db.employes:
            if id==emp.id:
                return emp
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    
    @post()
    async def create(self, data:db.Employee)->model.Employee:
        data.id=uuid.UUID()
        db.employes.append(data)
        return data
    
    @delete("/{id:uuid}")
    async def remove(self, id: uuid.UUID)->None:
        for emp in db.employes:
            if emp.id==id:
                db.employes.remove(emp)