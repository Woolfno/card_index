from uuid import UUID

from litestar import get
from litestar.controller import Controller
from pydantic import BaseModel

from models import models


class AJAXResponse(BaseModel):
    id: UUID
    parent: str = '#'
    text: str
    children:bool = True

def convert(items:list[models.Employee])->list[AJAXResponse]:
    res:list[AJAXResponse] = list()
    for item in items:
        response = AJAXResponse(id=item.id, text=item.full_name)
        if item.boss_id is not None:       
            response.parent = str(item.boss_id)
        res.append(response)
    return res


class AJAXEmployee(Controller):
    path = "/ajax"

    @get("/employee/")
    async def get_subordinates(self, id:str)->list[AJAXResponse]:
        query={"boss_id":None}
        try:
            query['boss_id'] = UUID(id)
        except ValueError:
            pass
        subordinates = await models.Employee.filter(**query)        
        return convert(subordinates)
