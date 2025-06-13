from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from uuid import uuid4



class HorseType(str, Enum):
    standard = "standard"
    legendary = "legendary"


class HorseCreate(BaseModel):
    name: str
    gender: str
    breed: str

    speed: float
    stamina: float
    strength: float
    jump: float
    height: float

    type: Optional[HorseType] = HorseType.standard
    stable_id: Optional[str] = None


class HorseResponse(BaseModel):
    id: str
    name: str
    gender: str
    breed: str

    speed: float
    stamina: float
    strength: float
    jump: float
    height: float
    age: int
    type: HorseType

    gene_speed: str
    gene_stamina: str
    gene_strength: str
    gene_jump: str

    owner_id: int
    stable_id: str
    is_pregnant: bool  # 🔧 ДОБАВЬ ЭТО СЮДА
    # можно также добавить pregnant_since: Optional[datetime] если нужно

    class Config:
        from_attributes = True



class HorseBreedRequest(BaseModel):
    mother_id: str
    father_id: str
    foal_name: str


class HorseUpdate(BaseModel):
    name: Optional[str] = None
    speed: Optional[float] = None
    stamina: Optional[float] = None
    strength: Optional[float] = None
    jump: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = Field(None, ge=0)
    type: Optional[HorseType] = None
