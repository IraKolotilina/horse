from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

# создаём движок на основании env
engine = create_engine(settings.DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Здесь при желании можно вызывать Base.metadata.create_all(engine)
    # из единственного места, где Base определён
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)
