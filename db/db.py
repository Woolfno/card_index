import datetime
import uuid
from decimal import Decimal

from tortoise import Tortoise, connections

from schemas.schemas import Employee, Position
from settings import settings

positions=[Position(id=0, title="Accountant"), Position(id=1, title="CEO")]
boss = Employee(id=uuid.uuid4(), first_name="Ivan",   middle_name="Petrovich", last_name="Smirnov", position=positions[1], start_date=datetime.date(2024, 1, 1), salary=Decimal(2500))
employes = [
    boss,
    Employee(id=uuid.uuid4(), boss=boss, first_name="Tomara", middle_name="Ivanovna",  last_name="Shpak",   position=positions[0], start_date=datetime.date(2024, 5, 2), salary=Decimal(500)),
]

async def init_tortoise()->None:
    await Tortoise.init(db_url=settings.DATABASE_URL, modules={"models": ["models.models"]})
    await Tortoise.generate_schemas()

async def shutdown_tortoise()->None:
    await connections.close_all()