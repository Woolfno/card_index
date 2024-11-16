from pydantic import BaseModel
from pydantic.config import ConfigDict
from tortoise.contrib.pydantic import pydantic_model_creator

from models.user import User as UserModel
from security.guard.roles import UserRole

UserPydantic = pydantic_model_creator(UserModel, name="User")

class User(UserPydantic):
    role:UserRole

    @property
    def is_guest(self)->bool:
        return self.role == UserRole.GUEST
    
    @property
    def is_authenticated(self)->bool:
        return self.role == UserRole.AUTHENTICATED

class UserIn(BaseModel):
    model_config =ConfigDict(from_attributes=True)

    username: str
    password: str
