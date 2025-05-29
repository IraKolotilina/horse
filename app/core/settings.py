# app/core/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"       # <- игнорируем DB_USER, DB_PASSWORD и прочие из .env
    )
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

settings = Settings()
