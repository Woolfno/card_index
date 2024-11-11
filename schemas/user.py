from models.user import User as UserModel
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel


UserPydantic = pydantic_model_creator(UserModel, name="User")

class UserIn(BaseModel):
    username: str
    password: str
