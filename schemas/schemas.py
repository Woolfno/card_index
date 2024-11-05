import datetime
import uuid
from decimal import Decimal
from typing import ForwardRef, Optional

from pydantic import BaseModel, Field, ConfigDict, computed_field


class PositionBase(BaseModel):
    id: int    

class Position(PositionBase):
    model_config=ConfigDict(from_attributes=True)

    title: str

class PositionIn(BaseModel):
    title: str

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