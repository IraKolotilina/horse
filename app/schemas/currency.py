# app/schemas/currency.py
from pydantic import BaseModel

class CurrencyUpdate(BaseModel):
    real: int
    game: int

class CurrencyOut(BaseModel):
    real_currency: int
    game_currency: int

    class Config:
        orm_mode = True
