from pydantic import BaseModel
from pydantic.config import ConfigDict
from tortoise.contrib.pydantic import pydantic_model_creator

from models.user import User as UserModel

UserPydantic = pydantic_model_creator(UserModel, name="User")


class UserIn(BaseModel):
    model_config =ConfigDict(from_attributes=True)

    username: str
    password: str
