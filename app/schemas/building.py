# app/schemas/building.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BuildingResponse(BaseModel):
    id: int
    type: str
    level: int
    created_at: datetime

    class Config:
        from_attributes = True
