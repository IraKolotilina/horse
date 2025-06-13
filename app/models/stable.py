import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Stable(Base):
    __tablename__ = "stables"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  # ✅ авто-UUID
    name = Column(String, nullable=False)
    level = Column(Integer, default=1)
    owner_id = Column(Integer, ForeignKey("players.id"))

    owner = relationship("Player", back_populates="stables")
    boxes = relationship("Box", back_populates="stable", cascade="all, delete-orphan")
    horses = relationship("Horse", back_populates="stable", cascade="all, delete-orphan")
    buildings = relationship("Building", back_populates="stable", cascade="all, delete-orphan")
