from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Box(Base):
    __tablename__ = "boxes"
    __table_args__ = {"extend_existing": True}

    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String, nullable=False)
    stable_id = Column(Integer, ForeignKey("stables.id"), nullable=False)

    stable    = relationship("Stable", back_populates="boxes")
