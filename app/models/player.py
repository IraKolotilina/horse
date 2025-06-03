# app/models/player.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base

class Player(Base):
    __tablename__ = "players"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String, unique=True, index=True, nullable=False)
    email         = Column(String, unique=True, index=True, nullable=False)
    password      = Column(String, nullable=False)
    last_login    = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


    real_currency = Column(Integer, default=0)
    game_currency = Column(Integer, default=0)
    buildings = relationship("Building", back_populates="owner")
    stables = relationship("Stable", back_populates="owner", cascade="all, delete-orphan")
    horses = relationship("Horse", back_populates="owner", cascade="all, delete-orphan")
