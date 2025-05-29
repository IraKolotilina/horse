# app/schemas/stable.py
from pydantic import BaseModel
from typing import List

class BoxOut(BaseModel):
    id: int
    name: str
    capacity: int
    stable_id: int

    class Config:
        orm_mode = True

class StableCreate(BaseModel):
    name: str

class StableOut(BaseModel):
    id: int
    name: str
    level: int
    owner_id: int
    boxes: List[BoxOut] = []

    class Config:
        orm_mode = True
