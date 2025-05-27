from pydantic import BaseModel, Field

class CurrencyBase(BaseModel):
    real_currency: int = Field(0, ge=0)
    game_currency: int = Field(0, ge=0)

class CurrencyUpdate(BaseModel):
    # can be negative here when PATCHing
    real_currency: int = 0
    game_currency: int = 0

class CurrencyResponse(CurrencyBase):
    class Config:
        orm_mode = True
