from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    host:str="127.0.0.1"
    port:int=8000
    DATABASE_URL:str
    SECRET_KEY:str
    JWT_ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    MEDIA_URL: str = "/media"
    MEDIA_ROOT: Path = Path(__file__).parent / "media"

settings = Settings()