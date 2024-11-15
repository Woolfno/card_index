from litestar import Controller, get, post
from schemas.position import Position, PositionIn
from models import models


class PositionController(Controller):
    path = "/position"

    @post()
    async def create(self, data:PositionIn)->Position:
        pos = await models.Position.create(**data.model_dump())
        return Position.model_validate(pos)