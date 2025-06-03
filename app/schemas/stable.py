# app/schemas/stable.py
from pydantic import BaseModel, ConfigDict
from typing import List

class BoxOut(BaseModel):
    id: int
    name: str
    capacity: int
    stable_id: str  # Было: int — ⚠ тип UUID = str
    model_config = ConfigDict(from_attributes=True)

class StableCreate(BaseModel):
    name: str

class StableOut(BaseModel):
    id: str  # ← Было: int, а в базе UUID → str
    name: str
    level: int
    owner_id: int
    boxes: List[BoxOut] = []
    model_config = ConfigDict(from_attributes=True)
