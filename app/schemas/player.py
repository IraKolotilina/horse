# app/schemas/player.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic import ConfigDict

class PlayerCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class PlayerOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class PlayerUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str]   = None

model_config = ConfigDict(from_attributes=True)