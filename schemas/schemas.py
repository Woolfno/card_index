import uuid
from pydantic import BaseModel
from typing import ForwardRef


class Position(BaseModel):
    id: int
    title: str

Employee = ForwardRef('Employee')

class Employee(BaseModel):
    id: uuid.UUID
    boss: Employee = None
    first_name: str
    middle_name: str
    last_name: str
    position: Position
    start_date: datetime.date
    salary: Decimal