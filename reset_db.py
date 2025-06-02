import psycopg2
from sqlalchemy import create_engine
from app.models.base import Base
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.core.config import settings  # берёт переменные из .env

# Данные из .env
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST
DB_PORT = "5432"  # при необходимости вынеси в .env
DATABASE_URL = settings.DATABASE_URL

# 1. Подключаемся к postgres
admin_conn = psycopg2.connect(
    dbname="postgres",
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
admin_conn.autocommit = True
admin_cursor = admin_conn.cursor()

print(f"🔁 Удаление и пересоздание базы данных: {DB_NAME}")

# 2. Drop и Create базы
admin_cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
admin_cursor.execute(f"CREATE DATABASE {DB_NAME};")

admin_cursor.close()
admin_conn.close()

# 3. Создание таблиц
print("📦 Создание таблиц в новой базе...")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

print("✅ База успешно пересоздана.")
