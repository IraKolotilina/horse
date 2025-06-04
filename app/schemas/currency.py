# app/schemas/currency.py
from pydantic import BaseModel, ConfigDict
from pydantic import ConfigDict
from typing import Optional

class CurrencyUpdate(BaseModel):
    real: Optional[int] = 0
    game: Optional[int] = 0

class CurrencyOut(BaseModel):
    real: int
    game: int


