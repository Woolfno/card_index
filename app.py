from litestar import Litestar, Router
from endpoints.employee import EmployeeController
from pydantic import BaseModel

from litestar import Litestar, post


app = Litestar(route_handlers=[
    Router(path="/", route_handlers=[EmployeeController]),
    ])