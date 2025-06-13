from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))

    type = Column(String, nullable=False)
    level = Column(Integer, default=1)

    stable_id = Column(String, ForeignKey("stables.id"))
    owner_id = Column(Integer, ForeignKey("players.id"))

    stable = relationship("Stable", back_populates="buildings")
    owner = relationship("Player", back_populates="buildings") 


