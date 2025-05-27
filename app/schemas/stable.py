from pydantic import BaseModel
from typing import List

class BoxResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True

class BuildingResponse(BaseModel):
    id: int
    type: str
    level: int

    class Config:
        from_attributes = True

class StableCreate(BaseModel):
    name: str

class StableResponse(BaseModel):
    id: int
    name: str
    level: int
    boxes: List[BoxResponse]
    buildings: List[BuildingResponse]

    class Config:
        from_attributes = True
