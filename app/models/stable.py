import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Stable(Base):
    __tablename__ = "stables"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  # <-- добавлен default
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    level = Column(Integer, default=1)
    


    owner = relationship("Player", back_populates="stables")
    boxes = relationship("Box", back_populates="stable", cascade="all, delete-orphan")
    horses = relationship("Horse", back_populates="stable", cascade="all, delete-orphan")
