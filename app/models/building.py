# app/models/building.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    stable_id = Column(Integer, ForeignKey("stables.id"), nullable=False)
    type = Column(String, nullable=False)
    level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    stable = relationship("Stable", back_populates="buildings")
