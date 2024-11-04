import datetime
import uuid
from decimal import Decimal
from typing import ForwardRef, Optional

from pydantic import BaseModel, Field, ConfigDict


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

    boss: Optional[Employee] = None  
    position: Position

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

    boss_id: Optional[uuid.UUID] = None  
    position: PositionIn