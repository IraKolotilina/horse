# app/core/settings.py
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field("your_secret_key", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
