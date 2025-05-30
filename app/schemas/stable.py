# app/schemas/stable.py
from pydantic import BaseModel, ConfigDict
from typing import List
from pydantic import ConfigDict

class BoxOut(BaseModel):
    id: int
    name: str
    capacity: int
    stable_id: int
    model_config = ConfigDict(from_attributes=True)

class StableCreate(BaseModel):
    name: str

class StableOut(BaseModel):
    id: int
    name: str
    level: int
    owner_id: int
    boxes: List[BoxOut] = []
    model_config = ConfigDict(from_attributes=True)
