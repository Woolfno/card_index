import datetime
import uuid
from decimal import Decimal
from typing import ForwardRef

from pydantic import BaseModel


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