from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    secret_key: str = Field("your_secret_key", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    database_url: str = Field("sqlite:///./test.db", env="DATABASE_URL")

    class Config:
        env_file = ".env"

settings = Settings()

# экспорт для удобства
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
DATABASE_URL = settings.database_url
