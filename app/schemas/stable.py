from pydantic import BaseModel

class StableCreate(BaseModel):
    name: str

class BoxResponse(BaseModel):
    id: int
    occupied: bool

    class Config:
        orm_mode = True

class BuildingResponse(BaseModel):
    id: int
    type: str
    level: int

    class Config:
        orm_mode = True

class StableResponse(BaseModel):
    id: int
    name: str
    level: int
    boxes: list[BoxResponse]
    buildings: list[BuildingResponse]

    class Config:
        orm_mode = True
