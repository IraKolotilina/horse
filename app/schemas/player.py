from pydantic import BaseModel, EmailStr
from typing import Optional

class PlayerCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class PlayerResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # актуально для Pydantic v2+

class PlayerUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

