# app/models/box.py

from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Box(Base):
    __tablename__ = "boxes"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    stable_id = Column(String, ForeignKey("stables.id"), nullable=False)

    stable = relationship("Stable", back_populates="boxes")
