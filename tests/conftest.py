import sys
from collections.abc import AsyncIterator
from pathlib import Path

import psycopg2
import pytest
import pytest_asyncio
from aerich import Command
from dotenv import dotenv_values
from litestar.testing import AsyncTestClient
from tortoise import Tortoise, connections

sys.path.append(str(Path(__file__).parent.parent))
from app import app
import generate_fake_data

app.debug = True

config = dotenv_values("tests/.env.test")
DATABASE_URL = config["DATABASE_URL"]

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models.models", "models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize():
    command = Command(tortoise_config=TORTOISE_ORM, app='models')

    async def init_db() -> None:
        await command.init()
        await command.upgrade()
        await generate_fake_data.run(TORTOISE_ORM)
        await Tortoise.init(TORTOISE_ORM)

    async def shutdown_db() -> None:
        await command.downgrade(version=-1, delete=False)
        await connections.close_all()

    app.on_startup = [init_db,]
    app.on_shutdown = [shutdown_db,]


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncIterator[AsyncTestClient]:
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest.fixture
def db():
    conn = psycopg2.connect(DATABASE_URL)
    yield conn
    conn.close()
