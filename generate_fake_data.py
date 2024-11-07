import random
import time
import argparse
from uuid import UUID

from faker import Faker
from fake_data.job_provider import JobProvider
from tortoise import Tortoise, run_async

from db.db import TORTOISE_ORM
from models.models import Employee, Position

MANAGERS = 5
SPECIALISTS = 20
OTHERS = 30

async def create_employee(fake:Faker, func_fake_position, boss_ids:list[UUID], count:int)->list[UUID]:
    empl_ids = []
    for i in range(count):
        position = Position(title=func_fake_position())
        await position.save()
        emp = await Employee.create(first_name=fake.first_name(), middle_name=fake.middle_name(), last_name=fake.last_name(), 
                        salary=random.randint(500, 3000), start_date=fake.date(), position_id=position.id, boss_id=random.choice(boss_ids))
        empl_ids.append(emp.uuid)
    
    return empl_ids

async def run():
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()

    random.seed(time.time())

    fake = Faker('ru_RU')
    fake.add_provider(JobProvider)

    # boss
    position = await Position.create(title="Директор")
    boss = await Employee.create(first_name=fake.first_name(), middle_name=fake.middle_name(), last_name=fake.last_name(), 
                        salary=random.randint(500, 3000), start_date=fake.date(), position_id=position.id, boss_id=None)

    # managers
    manager_ids = await create_employee(fake, fake.manager, [boss.uuid], MANAGERS)

    # specialists
    specialist_ids = await create_employee(fake, fake.specialist, manager_ids, SPECIALISTS)
    
    # other employees
    other_ids = await create_employee(fake, fake.other, specialist_ids, int(OTHERS*0.6))
    await create_employee(fake, fake.other, other_ids, int(OTHERS*0.4))

run_async(run())