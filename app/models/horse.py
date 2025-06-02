from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.models.base import Base

class Horse(Base):
    __tablename__ = "horses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    gender = Column(String, nullable=False)  # "stallion" or "mare"
    breed = Column(String, nullable=False)

    speed = Column(Float, nullable=False)
    stamina = Column(Float, nullable=False)
    strength = Column(Float, nullable=False)

    gene_speed = Column(String, nullable=False)
    gene_stamina = Column(String, nullable=False)
    gene_strength = Column(String, nullable=False)

    is_pregnant = Column(Boolean, default=False)
    pregnant_since = Column(DateTime, nullable=True)
    stable_id = Column(String, ForeignKey("stables.id"), nullable=True)

    # Обратная связь с владельцем
    owner = relationship("Player", back_populates="horses")
    stable = relationship("Stable", back_populates="horses")

    created_at = Column(DateTime, default=datetime.utcnow)
