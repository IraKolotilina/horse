from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    # connect_args={"check_same_thread": False}  # если SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# чтобы SQLAlchemy “видела” все модели при инициализации
import app.models.player
import app.models.building
import app.models.box
import app.models.stable

def init_db():
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    FastAPI-зависимость: возвращает сессию и гарантирует её .close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
