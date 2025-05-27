from pydantic import BaseModel, Field

class CurrencyResponse(BaseModel):
    real: int = Field(..., ge=0)
    game: int = Field(..., ge=0)

    class Config:
        from_attributes = True

class CurrencyUpdate(BaseModel):
    real: int = Field(..., ge=0)
    game: int = Field(..., ge=0)

class CurrencyPatch(BaseModel):
    real: int
    game: int
