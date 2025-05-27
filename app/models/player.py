from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    last_login = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- новые поля для валюты ---
    real_currency = Column(Float, default=0.0, nullable=False)
    game_currency = Column(Float, default=0.0, nullable=False)

    # отношение к Stable (если понадобится)
    stables = relationship("Stable", back_populates="player")
