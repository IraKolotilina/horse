from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Stable(Base):
    __tablename__ = "stables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    player = relationship("Player", back_populates="stables")
    boxes = relationship("Box", back_populates="stable", cascade="all, delete-orphan")
    buildings = relationship("Building", back_populates="stable", cascade="all, delete-orphan")
