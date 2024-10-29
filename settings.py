from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host:str="127.0.0.1"
    port:int=8000
    DATABASE_URL:str

settings = Settings()