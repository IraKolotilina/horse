from pydantic import BaseModel, ConfigDict

class BoxOut(BaseModel):
    id: str
    name: str
    stable_id: str

    model_config = ConfigDict(from_attributes=True)
