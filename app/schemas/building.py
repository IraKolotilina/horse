from pydantic import BaseModel

class BuildingResponse(BaseModel):
    id: int
    name: str
    level: int

    class Config:
        orm_mode = True
