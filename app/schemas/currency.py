# app/schemas/currency.py
from pydantic import BaseModel

class CurrencyResponse(BaseModel):
    real: int
    game: int

    class Config:
        from_attributes = True

class CurrencyUpdate(BaseModel):
    real: int
    game: int

class CurrencyChange(BaseModel):
    real: int = 0
    game: int = 0
