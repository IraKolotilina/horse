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

class HorseResponse(HorseCreate):
    id: str
    owner_id: int
    stable_id: Optional[str]
    gene_speed: str
    gene_stamina: str
    gene_strength: str
    is_pregnant: bool
    pregnant_since: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
