from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    stables = relationship("Stable", back_populates="owner")
    # buildings = relationship("Building", back_populates="player")  # <-- УДАЛИТЬ ЭТУ СТРОКУ!
    horses = relationship("Horse", back_populates="owner")
