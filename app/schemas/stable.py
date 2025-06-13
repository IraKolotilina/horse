from pydantic import BaseModel, ConfigDict, Field

class StableCreate(BaseModel):
    name: str

class StableOut(BaseModel):
    id: str
    name: str
    level: int
    model_config = ConfigDict(from_attributes=True)
