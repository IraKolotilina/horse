from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # читаем из .env, игнорируем все лишние переменные (DB_USER, DB_PASSWORD и т.п.)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    DATABASE_URL: str

settings = Settings()
