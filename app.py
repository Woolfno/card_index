import logging
from litestar import Litestar, Router
from endpoints.employee import EmployeeController
from db.db import init_tortoise, shutdown_tortoise
import uvicorn
from litestar import Litestar
from settings import settings


app = Litestar(    
    route_handlers=[
        Router(path="/", route_handlers=[EmployeeController]),
    ],
    on_startup=[init_tortoise],
    on_shutdown=[shutdown_tortoise],
    )

if __name__=="__main__":
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port
    )