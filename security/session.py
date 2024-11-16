from typing import Any, Dict, Optional
from uuid import UUID
from litestar.connection import ASGIConnection
from litestar.middleware.session.client_side import CookieBackendConfig, ClientSideSessionBackend
from litestar.middleware.session.server_side import ServerSideSessionBackend
from litestar.security.session_auth import SessionAuth

from security.guard.roles import UserRole
from models.user import User as UserModel
from schemas.user import User
from settings import settings


async def retrieve_user_handler(session:Dict[str,Any],connection:"ASGIConnection[Any, Any, Any, Any]")->Optional[User]:
    u = await UserModel.get_or_none(id=session.get("user_id"))    
    if u is None:
        return User(id=UUID(0,0) ,username="guest", role=UserRole.GUEST)
    user =  User.model_construct(**u.__dict__, role=UserRole.AUTHENTICATED)
    return user

session_auth = SessionAuth[User, ClientSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=CookieBackendConfig(secret=settings.SECRET_KEY.encode("utf-8")[:24]),
    exclude=["/login", "/singup", "/api/auth", "/schema"],
)