from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class BoxOut(BaseModel):
    id: int
    name: str
    capacity: int
    stable_id: str  # исправлено с int → str (Stable.id = str / UUID)
    model_config = ConfigDict(from_attributes=True)


class StableCreate(BaseModel):
    name: str


class StableOut(BaseModel):
    id: str
    name: str
    level: int
    owner_id: Optional[int]  # можно убрать или скрыть на фронте
    boxes: List[BoxOut] = []
    model_config = ConfigDict(from_attributes=True)
