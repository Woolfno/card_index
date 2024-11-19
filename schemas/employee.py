import datetime
import uuid
from decimal import Decimal
from typing import ForwardRef, Optional
from schemas.position import Position
from litestar.datastructures import UploadFile
from pydantic import BaseModel, Field, ConfigDict, computed_field


Employee = ForwardRef('Employee')

class EmployeeId(BaseModel):    
    id: uuid.UUID = Field(alias="uuid")

class EmployeeBase(EmployeeId): 
    first_name: str
    middle_name: str
    last_name: str   
    start_date: datetime.date
    salary: Decimal

class Employee(EmployeeBase):   
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(exclude=True)
    middle_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)
    boss: Optional[Employee] = None
    position: Position

    @computed_field
    def full_name(self)->str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"

class EmployeeIn(BaseModel):
    first_name: str
    middle_name: str
    last_name: str   
    start_date: datetime.date
    salary: Decimal
    position_id: int
    boss_id: uuid.UUID = None

class EmployeeAll(EmployeeBase):   
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(exclude=True)
    middle_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)
    boss_id: Optional[uuid.UUID] = None
    position: Position

    @computed_field
    def full_name(self)->str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    
class EmployeeWithPhoto(EmployeeIn):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    photo_file: Optional[UploadFile] = None
