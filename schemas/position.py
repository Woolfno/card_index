from pydantic import BaseModel, Field, ConfigDict, computed_field


class PositionBase(BaseModel):
    id: int    

class Position(PositionBase):
    model_config=ConfigDict(from_attributes=True)

    title: str

class PositionIn(BaseModel):
    title: str