from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    stable_id = Column(String, ForeignKey("stables.id"), nullable=False)
    owner_id = Column(String, ForeignKey("players.id"), nullable=False)  # ОБЯЗАТЕЛЬНО!
    
    
    stable = relationship("Stable", back_populates="buildings")
    owner = relationship("Player", back_populates="buildings")
