from pathlib import Path

import uvicorn
from litestar import HttpMethod, Litestar, Request, Router, get, route
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from db.db import init_tortoise, shutdown_tortoise
from endpoints.auth import AuthController
from endpoints.employee import EmployeeController
from endpoints.position import PositionController
from security.jwt import authenticate_user, jwt_auth
from settings import settings


@get("/", exclude_from_auth=True)
async def index()->Template:
    return Template(template_name="index.html", context={"main":True})

@get("/tree")
async def tree()->Template:
    return Template(template_name="tree.html", context={"tree":True})

@get('/table')
async def employees()->Template:
    return Template(template_name='table.html', context={"table":True})

@route(path='/login', http_method=[HttpMethod.GET, HttpMethod.POST])  
async def login(request:Request)->Template:    
    if request.method==HttpMethod.GET:
        return Template(template_name="login.html", context={"login":True})

    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    user = await authenticate_user(username, password)
    if user is None:
        return Template(template_name="login.html", context={
            "login":True,
            "err":"Неверное имя пользователя или пароль!"
        })
    return jwt_auth.login(identifier=user.id)

apiRoute = Router(path="/api", route_handlers=[EmployeeController, PositionController, AuthController])

app = Litestar(    
    route_handlers=[
        create_static_files_router(path="/static", directories=[Path(__file__).parent / "static"]),
        index, tree, employees, login, 
        apiRoute,
    ],
    template_config=TemplateConfig(directory=Path(__file__).parent / "template", engine=JinjaTemplateEngine),    
    on_startup=[init_tortoise],
    on_shutdown=[shutdown_tortoise],
    on_app_init=[jwt_auth.on_app_init],
    )

if __name__=="__main__":
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port
    )