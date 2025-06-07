from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Boolean, Integer, Enum as PgEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from enum import Enum


class HorseType(str, Enum):
    standard = "standard"
    legendary = "legendary"


class Horse(Base):
    __tablename__ = "horses"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    breed = Column(String, nullable=False)

    speed = Column(Float, nullable=False)
    stamina = Column(Float, nullable=False)
    strength = Column(Float, nullable=False)
    jump = Column(Float, nullable=False)  # ✅ Новый параметр — прыжки

    height = Column(Float, nullable=False)  # ✅ Рост
    age = Column(Integer, default=0)        # ✅ Возраст
    type = Column(PgEnum(HorseType), default=HorseType.standard)  # ✅ Тип лошади: стандарт / легенда

    gene_speed = Column(String, nullable=False)
    gene_stamina = Column(String, nullable=False)
    gene_strength = Column(String, nullable=False)
    gene_jump = Column(String, nullable=False)


    is_pregnant = Column(Boolean, default=False)
    pregnant_since = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("players.id"))
    stable_id = Column(String, ForeignKey("stables.id"))

    owner = relationship("Player", back_populates="horses")     # ✅ Обратная связь с владельцем
    stable = relationship("Stable", back_populates="horses")    # ✅ Обратная связь с конюшней


