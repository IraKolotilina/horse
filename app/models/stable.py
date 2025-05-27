# app/models/stable.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Stable(Base):
    __tablename__ = "stables"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    name = Column(String, nullable=False)
    level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("Player", back_populates="stables")
    boxes = relationship("Box", back_populates="stable")
    buildings = relationship("Building", back_populates="stable")
