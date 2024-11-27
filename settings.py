from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    host:str="127.0.0.1"
    port:int=8000
    DATABASE_URL:str
    SECRET_KEY:str = "6535dffc2d75060e9960b147af7a0f025ad4db5112a643e93256dc6e542fa6b1"
    JWT_ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 10
    MEDIA_URL: str = "/media"
    MEDIA_ROOT: Path = Path(__file__).parent / "media"

settings = Settings()