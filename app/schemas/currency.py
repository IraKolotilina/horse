# app/schemas/currency.py
from pydantic import BaseModel, ConfigDict
from pydantic import ConfigDict
from typing import Optional


class CurrencyUpdate(BaseModel):
    real: int = 0
    game: int = 0

class CurrencyOut(BaseModel):
    real: int
    game: int

