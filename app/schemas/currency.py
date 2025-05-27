from pydantic import BaseModel
from typing import Optional

class CurrencyBase(BaseModel):
    real_currency: float
    game_currency: int

class CurrencyResponse(CurrencyBase):
    class Config:
        orm_mode = True

class CurrencyUpdate(CurrencyBase):
    pass

class CurrencyPatch(BaseModel):
    real_currency: Optional[float] = 0.0
    game_currency: Optional[int] = 0
