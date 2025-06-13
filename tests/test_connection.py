import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine


client = TestClient(app)


url = "postgresql://horse_user:horse_pass@localhost/horse_game_db"
engine = create_engine(url)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Успешное подключение к БД!")
except Exception as e:
    print("❌ Ошибка подключения:", e)
