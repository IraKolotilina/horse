# app/core/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # JWT
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str  = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Database
    database_url: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# backwards‐compatible module‐level names
SECRET_KEY = settings.secret_key
ALGORITHM  = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
DATABASE_URL = settings.database_url
