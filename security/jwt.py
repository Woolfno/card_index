from datetime import timedelta
from typing import Any, Optional

from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, JWTCookieAuth, Token

from models.user import User as UserModel
from schemas.user import UserPydantic as UserSchema
from settings import settings


async def retrieve_user_handler(token: Token, connection: "ASGIConnection[Any, Any, Any, Any]") -> Optional[UserSchema]:
    user = await UserModel.get_or_none(id=token.sub)
    if user is None:
        return None
    return UserSchema.model_validate(user)

jwt_auth = JWTAuth[UserSchema](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.SECRET_KEY,
    default_token_expiration=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    exclude=["/login", "/singup", "/api/auth", "/schema"],
)

jwt_cookie_auth = JWTCookieAuth[UserSchema](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.SECRET_KEY,
    default_token_expiration=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    exclude=["/auth","/login", "/singup", "/schema"]
)