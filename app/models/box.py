from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Box(Base):
    __tablename__ = "boxes"
    id = Column(Integer, primary_key=True, index=True)
    stable_id = Column(Integer, ForeignKey("stables.id"), nullable=False)

    stable = relationship("Stable", back_populates="boxes")
