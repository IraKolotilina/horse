from typing import Optional
from app.models.player import Player
from sqlalchemy import create_engine, text


url = "postgresql://horse_user:horse_pass@localhost/horse_game_db"
engine = create_engine(url)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Успешное подключение к БД!")
except Exception as e:
    print("❌ Ошибка подключения:", e)
