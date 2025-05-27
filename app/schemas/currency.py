from pydantic import BaseModel, Field

class CurrencyUpdate(BaseModel):
    real_currency: int = Field(0, ge=0)
    game_currency: int = Field(0, ge=0)

class CurrencyPatch(BaseModel):
    real_currency: int = Field(0)
    game_currency: int = Field(0)

class CurrencyResponse(BaseModel):
    real_currency: int
    game_currency: int

    class Config:
        orm_mode = True
