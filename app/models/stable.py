from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Stable(Base):
    __tablename__ = "stables"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("players.id"))
    owner = relationship("Player", back_populates="stables")
    buildings = relationship("Building", back_populates="stable", cascade="all, delete")
