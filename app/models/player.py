from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    real_currency = Column(Float, default=0.0)  # <--- добавь это поле!

    stables = relationship("Stable", back_populates="owner")
    horses = relationship("Horse", back_populates="owner")
    buildings = relationship("Building", back_populates="owner")  # <--- ВАЖНО! (исправляет ошибку)
