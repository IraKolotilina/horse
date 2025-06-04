# app/schemas/box.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class BoxResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
