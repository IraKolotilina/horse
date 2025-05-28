# app/models/stable.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Stable(Base):
    __tablename__ = "stables"
    __table_args__ = {"extend_existing": True}

    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String, nullable=False)
    owner_id  = Column(Integer, ForeignKey("players.id"), nullable=False)
    level     = Column(Integer, default=1)

    owner     = relationship("Player", back_populates="stables")
    boxes     = relationship("Box", back_populates="stable")
    building  = relationship("Building", back_populates="owner")
