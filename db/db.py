from pydantic import BaseModel
from typing import ForwardRef
import datetime
import uuid
from decimal import Decimal


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


positions=[Position(id=0, title="Accountant"), Position(id=1, title="CEO")]
boss = Employee(id=uuid.uuid4(), first_name="Ivan",   middle_name="Petrovich", last_name="Smirnov", position=positions[1], start_date=datetime.date(2024, 1, 1), salary=Decimal(2500))
employes = [
    boss,
    Employee(id=uuid.uuid4(), boss=boss, first_name="Tomara", middle_name="Ivanovna",  last_name="Shpak",   position=positions[0], start_date=datetime.date(2024, 5, 2), salary=Decimal(500)),
]