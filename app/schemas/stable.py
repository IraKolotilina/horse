from pydantic import BaseModel, Field
from typing import Optional, List


class StableCreate(BaseModel):
    name: str


class StableOut(BaseModel):
    id: str
    name: str
    level: int

    class Config:
        from_attributes = True


class BoxOut(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class BuildingCreate(BaseModel):
    type: str
    level: int = Field(..., ge=1)


class BuildingOut(BaseModel):
    id: str
    type: str
    level: int
    stable_id: str

    class Config:
        from_attributes = True
