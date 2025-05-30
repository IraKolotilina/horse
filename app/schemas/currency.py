# app/schemas/currency.py
from pydantic import BaseModel, ConfigDict
from pydantic import ConfigDict

class CurrencyUpdate(BaseModel):
    real: int
    game: int

class CurrencyOut(BaseModel):
    real_currency: int
    game_currency: int
    model_config = ConfigDict(from_attributes=True)
