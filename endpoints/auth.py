from litestar import Response, post
from litestar.controller import Controller
from litestar.exceptions import HTTPException, NotAuthorizedException
from tortoise.exceptions import IntegrityError

from models.user import User as UserModel
from schemas.user import UserIn as UserSchema
from schemas.user import UserPydantic
from security.jwt import authenticate_user, get_password_hash, jwt_auth


class AuthController(Controller):
    path = "/auth"

    @post("login")
    async def login(data:UserSchema)->Response[UserPydantic]:
        user = await authenticate_user(data.username, data.password)
        if user is None:
            raise NotAuthorizedException    
        return jwt_auth.login(identifier=str(user.id))

    @post("signup")
    async def signup(data:UserSchema)->Response[UserPydantic]:
        try:
            user = await UserModel.create(username=data.username, password_hash=get_password_hash(data.password))
        except IntegrityError:
            raise HTTPException(detail=f"{data.username} is exists", status_code=400)
        if user is None:
            return HTTPException(detail="not registration", status_code=400)
        return Response(UserPydantic.model_validate(user))
