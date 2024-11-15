from typing import Any, Dict, Optional

from litestar.connection import ASGIConnection
from litestar.middleware.session.client_side import CookieBackendConfig
from litestar.middleware.session.server_side import ServerSideSessionBackend
from litestar.security.session_auth import SessionAuth

from models.user import User
from schemas.user import UserPydantic
from settings import settings

session_config = CookieBackendConfig(secret=settings.SECRET_KEY.encode("utf-8")[:24])

async def retrieve_user_handler(session:Dict[str,Any],connection:"ASGIConnection[Any, Any, Any, Any]")->Optional[User]:
    return await User.get_or_none(id=session.get("user_id"))

session_auth = SessionAuth[UserPydantic, ServerSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=CookieBackendConfig(secret=settings.SECRET_KEY.encode("utf-8")[:24]),
    exclude=["/login", "/singup", "/api/auth", "/schema"],
)