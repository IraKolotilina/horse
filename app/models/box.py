# app/models/box.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Box(Base):
    __tablename__ = "boxes"

    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String, nullable=False)
    capacity  = Column(Integer, default=1)
    stable_id = Column(Integer, ForeignKey("stables.id"), nullable=False)

    stable = relationship("Stable", back_populates="boxes")
