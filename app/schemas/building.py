from pydantic import BaseModel, ConfigDict, Field

class BuildingCreate(BaseModel):
    type: str
    level: int = Field(..., ge=1)

class BuildingOut(BaseModel):
    id: str
    type: str
    level: int
    stable_id: str

    model_config = ConfigDict(from_attributes=True)
