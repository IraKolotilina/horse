# app/schemas/player.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class PlayerCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class PlayerOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    last_login: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True

class PlayerUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str]   = None
