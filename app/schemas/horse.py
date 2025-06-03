from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class HorseCreate(BaseModel):
    name: str
    gender: str
    breed: str
    speed: float
    stamina: float
    strength: float
    stable_id: Optional[str]  # 👈 строка, так как это UUID в String-формате

class HorseResponse(HorseCreate):
    id: str  # 👈 UUID строкой
    owner_id: int
    gene_speed: str
    gene_stamina: str
    gene_strength: str
    is_pregnant: bool
    pregnant_since: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
