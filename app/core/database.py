from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import DATABASE_URL
from app.models.base import Base   # у тебя уже есть

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
