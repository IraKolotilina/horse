from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    secret_key: str = Field("your_secret_key", env="SECRET_KEY")
    database_url: str = Field(
        "postgresql://horse_user:horse_pass@localhost/horse_game_db",
        env="DATABASE_URL",
    )

    class Config:
        extra = "ignore"
        env_file = ".env"

settings = Settings()
