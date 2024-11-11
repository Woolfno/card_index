from litestar import Controller, get, post
from schemas import schemas
from models import models


class PositionController(Controller):
    path = "/position"

    @post()
    async def create(self, data:schemas.PositionIn)->schemas.Position:
        pos = await models.Position.create(**data.model_dump())
        return schemas.Position.model_validate(pos)