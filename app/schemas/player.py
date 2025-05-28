from typing import Optional
from pydantic import BaseModel
from app.core.security import hash_password


class PlayerCreate(BaseModel):
    username: str
    email: str
    password: str

class PlayerResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class PlayerUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

# ↓↓↓ Новые схемы
class CurrencyResponse(BaseModel):
    real: int
    game: int

    class Config:
        from_attributes = True

class CurrencySet(BaseModel):
    real: int
    game: int

class CurrencyDelta(BaseModel):
    real: Optional[int] = 0
    game: Optional[int] = 0
