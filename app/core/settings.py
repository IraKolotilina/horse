import os

# секрет для JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# URL БД
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://horse_user:horse_pass@localhost/horse_game_db"
)
