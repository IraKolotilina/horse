# убрали Pydantic BaseSettings, оставили простой класс
class Settings:
    # секрет для JWT
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # строка подключения к БД; подменяйте под prod
    database_url: str = "sqlite:///./test.db"


settings = Settings()

# экспорты для удобства
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
DATABASE_URL = settings.database_url
