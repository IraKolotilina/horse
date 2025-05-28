from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Player(Base):
    __tablename__ = "players"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String, unique=True, index=True, nullable=False)
    email         = Column(String, unique=True, index=True, nullable=False)
    password      = Column(String, nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    last_login    = Column(DateTime(timezone=True), onupdate=func.now())

    real_currency = Column(Integer, default=0, nullable=False)
    game_currency = Column(Integer, default=0, nullable=False)

    # связи
    buildings = relationship("Building", back_populates="owner", cascade="all, delete")
    boxes     = relationship("Box",      back_populates="stable", cascade="all, delete")
    stables   = relationship("Stable",   back_populates="owner", cascade="all, delete")
