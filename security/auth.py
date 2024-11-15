from passlib.context import CryptContext

from models.user import User as UserModel

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