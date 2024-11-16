from pathlib import Path

import uvicorn
from litestar import Litestar, Router
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from controllers.api import auth_router, employee_router, position_router
from controllers.html.html import HTMLController
from db.db import init_tortoise, shutdown_tortoise
from security.jwt import jwt_auth
from security.session import session_auth
from settings import settings

apiRoute = Router(path="/api", route_handlers=[employee_router, position_router, auth_router])

app = Litestar(    
    route_handlers=[
        create_static_files_router(path="/static", directories=[Path(__file__).parent / "static"]),        
        Router(path="/", route_handlers=[HTMLController]),
        apiRoute,
    ],
    template_config=TemplateConfig(directory=Path(__file__).parent / "templates", engine=JinjaTemplateEngine),    
    on_startup=[init_tortoise],
    on_shutdown=[shutdown_tortoise],
    # on_app_init=[session_auth.on_app_init],
    )

if __name__=="__main__":
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port
    )