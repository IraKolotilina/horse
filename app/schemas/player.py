from pydantic import BaseModel, EmailStr, Field

class PlayerBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr

class PlayerCreate(PlayerBase):
    password: str = Field(..., min_length=6)

class PlayerUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None   = None

class PlayerOut(PlayerBase):
    id: int
    real_currency: int
    game_currency: int

    class Config:
        from_attributes = True
