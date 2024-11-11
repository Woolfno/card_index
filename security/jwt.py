from datetime import timedelta
from typing import Any, Optional

from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth
from passlib.context import CryptContext

from models.user import User as UserModel
from schemas.token import Token
from schemas.user import UserPydantic as UserSchema
from settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str)->str:
    return pwd_context.hash(password)

async def authenticate_user(username:str, password:str)->UserModel:
    user = await UserModel.get_or_none(username=username)
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

async def retrieve_user_handler(token: Token, connection: "ASGIConnection[Any, Any, Any, Any]") -> Optional[UserModel]:
    return await UserModel.get_or_none(id=token.sub)

jwt_auth = JWTAuth[UserSchema](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.SECRET_KEY,
    default_token_expiration=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    exclude=["/signup", "/login", "/authenticate", "/schema"],
)