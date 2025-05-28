# app/models/player.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models.base import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    last_login = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ← NEW
    real_currency = Column(Integer, default=0, nullable=False)
    game_currency = Column(Integer, default=0, nullable=False)
