from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Stable(Base):
    __tablename__ = "stables"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, default=1)
    owner_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    owner = relationship("Player", back_populates="stables")
    boxes = relationship("Box", back_populates="stable")
    buildings = relationship("Building", back_populates="stable")

class Box(Base):
    __tablename__ = "boxes"
    id = Column(Integer, primary_key=True)
    stable_id = Column(Integer, ForeignKey("stables.id"), nullable=False)
    occupied = Column(Integer, default=False)

    stable = relationship("Stable", back_populates="boxes")

class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True)
    stable_id = Column(Integer, ForeignKey("stables.id"), nullable=False)
    type = Column(String, nullable=False)
    level = Column(Integer, default=1)

    stable = relationship("Stable", back_populates="buildings")
