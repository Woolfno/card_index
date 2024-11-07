from pathlib import Path

import uvicorn
from litestar import Litestar, Router, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar.static_files import create_static_files_router

from db.db import init_tortoise, shutdown_tortoise
from endpoints.employee import EmployeeController
from endpoints.position import PositionController
from settings import settings

@get("/")
async def index()->Template:
    return Template(template_name="index.html")

@get("/tree")
async def tree()->Template:
    return Template(template_name="tree.html")

@get('/table')
async def employees()->Template:
    return Template(template_name='list.html')

app = Litestar(    
    route_handlers=[
        create_static_files_router(path="/static", directories=[Path(__file__).parent / "static"]),
        index, tree, employees,
        Router(path="/", route_handlers=[EmployeeController, PositionController]),
    ],
    template_config=TemplateConfig(directory=Path(__file__).parent / "template", engine=JinjaTemplateEngine),    
    on_startup=[init_tortoise],
    on_shutdown=[shutdown_tortoise],
    )

if __name__=="__main__":
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port
    )