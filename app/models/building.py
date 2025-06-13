from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Building(Base):
    __tablename__ = "buildings"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    type = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    stable_id = Column(String, ForeignKey("stables.id"), nullable=False)

    stable = relationship("Stable", back_populates="buildings")
