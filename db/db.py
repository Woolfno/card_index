from tortoise import Tortoise, connections

from settings import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init_tortoise()->None:
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def shutdown_tortoise()->None:
    await connections.close_all()