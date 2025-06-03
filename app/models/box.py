# app/models/box.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Box(Base):
    __tablename__ = "boxes"

    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String, nullable=False)
    capacity  = Column(Integer, default=1)
    stable_id = Column(String, ForeignKey("stables.id"), nullable=True)  # <-- исправлено с Integer на String

    stable = relationship("Stable", back_populates="boxes")
