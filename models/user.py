from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.UUIDField(primary_key=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=256, null=True)

    class PydanticMeta:
        exclude = ["password_hash"]