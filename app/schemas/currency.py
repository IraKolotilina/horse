# app/schemas/currency.py
from pydantic import BaseModel

class Currency(BaseModel):
    real: int
    game: int

    class Config:
        orm_mode = True
