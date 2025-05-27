from pydantic import BaseModel

class StableCreate(BaseModel):
    name: str

class StableResponse(BaseModel):
    id: int
    name: str
    level: int

    class Config:
        from_attributes = True
