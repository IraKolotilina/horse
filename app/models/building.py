# app/models/building.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base   # ← same Base everywhere

class Building(Base):
    __tablename__ = "buildings"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String, nullable=False)
    level    = Column(Integer, default=1)
    owner_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    owner = relationship("Player", back_populates="buildings")
