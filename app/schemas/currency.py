from pydantic import BaseModel

class CurrencyResponse(BaseModel):
    real: float
    game: float

    class Config:
        from_attributes = True

class CurrencyUpdate(BaseModel):
    real: float
    game: float

class CurrencyChange(BaseModel):
    real: float = 0.0
    game: float = 0.0
