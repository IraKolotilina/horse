# reset_db.py
import psycopg2
from sqlalchemy import create_engine
from app.models.base import Base
import sys
import os
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import app.models.player
import app.models.stable
import app.models.building
import app.models.box
import app.models.horse


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.core.config import settings  # берёт переменные из .env

# Данные из .env
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST
DB_PORT = "5432"  # Можно вынести в .env при необходимости
DATABASE_URL = settings.DATABASE_URL

# 1. Подключение к postgres для администрирования
print(f"🔁 Удаление и пересоздание базы данных: {DB_NAME}")
try:
    admin_conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    admin_cursor = admin_conn.cursor()

    # 2. Завершение активных подключений к БД (иначе DROP может упасть)
    admin_cursor.execute(f"""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{DB_NAME}' AND pid <> pg_backend_pid();
    """)

    admin_cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
    admin_cursor.execute(f"CREATE DATABASE {DB_NAME};")

    admin_cursor.close()
    admin_conn.close()

    print("📦 Создание таблиц в новой базе...")

    # 3. Подключение к новой БД и создание таблиц
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    print("✅ База успешно пересоздана.")
except Exception as e:
    print("❌ Ошибка при пересоздании базы:", e)
