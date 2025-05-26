from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    stable_id = Column(Integer, ForeignKey("stables.id"))
    type = Column(String, nullable=False)  # e.g., "administration", "stable", "track"
    level = Column(Integer, default=1)
    stable = relationship("Stable", back_populates="buildings")

    __table_args__ = (
        UniqueConstraint('stable_id', 'type',
                         name='one_building_type_per_stable'),
    )
