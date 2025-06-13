from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class StableCreate(BaseModel):
    name: str

class StableOut(BaseModel):
    id: str
    name: str
    level: int
    model_config = ConfigDict(from_attributes=True)

class BoxOut(BaseModel):
    id: str
    name: str
    model_config = ConfigDict(from_attributes=True)

class BuildingCreate(BaseModel):
    type: str
    level: int = Field(..., ge=1)

class BuildingOut(BaseModel):
    id: str
    type: str
    level: int
    stable_id: str
    model_config = ConfigDict(from_attributes=True)
