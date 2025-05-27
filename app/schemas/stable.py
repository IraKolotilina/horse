# app/schemas/stable.py
from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemas.box import BoxResponse
from app.schemas.building import BuildingResponse

class StableCreate(BaseModel):
    name: str

class StableResponse(BaseModel):
    id: int
    name: str
    level: int
    created_at: datetime
    boxes: List[BoxResponse]
    buildings: List[BuildingResponse]

    class Config:
        from_attributes = True
