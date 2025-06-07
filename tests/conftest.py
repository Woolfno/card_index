import pytest
import pytest_asyncio
from collections.abc import AsyncIterator
from tortoise import Tortoise, connections
from litestar.testing import AsyncTestClient
from aerich import Command
import generate_fake_data
import psycopg2
from app import app

app.debug = True

DATABASE_URL = "postgres://postgres:postgres@192.168.1.115:5432/cardindex_test"

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
    async def init_db()->None:
        await command.init()
        await command.upgrade()
        await generate_fake_data.run(TORTOISE_ORM)
        await Tortoise.init(TORTOISE_ORM)
        
    async def shutdown_db()->None:
        await command.downgrade(version=-1, delete=False)
        await connections.close_all()

    app.on_startup = [init_db,]
    app.on_shutdown = [shutdown_db,]

@pytest_asyncio.fixture
async def client()->AsyncIterator[AsyncTestClient]:
    async with AsyncTestClient(app=app) as client:
        yield client

@pytest.fixture
def db():
    conn = psycopg2.connect(DATABASE_URL)
    yield conn
    conn.close()