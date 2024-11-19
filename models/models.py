import datetime

from tortoise import fields
from tortoise.models import Model


class Position(Model):
    id=fields.IntField(primary_key=True)
    title = fields.CharField(max_length=100)

    class Meta:
        ordering = ["title"]

class Employee(Model):
    uuid = fields.UUIDField(primary_key=True)
    boss = fields.ForeignKeyField("models.Employee", on_delete=fields.SET_NULL, null=True)
    first_name = fields.CharField(max_length=120)
    middle_name = fields.CharField(max_length=120)
    last_name = fields.CharField(max_length=120)
    position = fields.ForeignKeyField("models.Position", related_name="employes")
    start_date = fields.DateField(default=datetime.datetime.now)
    salary = fields.DecimalField(max_digits=8, decimal_places=2)
    photo_url = fields.CharField(max_length=255, null=True)

    @property
    def full_name(self)->str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
