from pydantic import BaseModel, Field


class BuildingCreate(BaseModel):
    type: str
    level: int = Field(..., ge=1)


class BuildingOut(BaseModel):
    id: str
    type: str
    level: int
    stable_id: str

    class Config:
        from_attributes = True
