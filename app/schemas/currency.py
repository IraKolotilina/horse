from pydantic import BaseModel, conint

class Currency(BaseModel):
    real_currency: int
    game_currency: int

class CurrencyUpdate(BaseModel):
    real_currency: conint(ge=0)
    game_currency: conint(ge=0)

class CurrencyDelta(BaseModel):
    real_delta: int
    game_delta: int
