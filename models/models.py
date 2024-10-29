import datetime

from tortoise.models import Model
from tortoise import fields

class Position(Model):
    id=fields.IntField(primary_key=True)
    title = fields.CharField(max_length=100)

class Employee(Model):
    uuid = fields.UUIDField(primary_key=True)
    boss = fields.ForeignKeyField("models.Employee", on_delete=fields.SET_NULL, null=True)
    first_name = fields.CharField(max_length=120)
    middle_name = fields.CharField(max_length=120)
    last_name = fields.CharField(max_length=120)
    position = fields.ForeignKeyField("models.Position", related_name="employes")
    start_date = fields.DateField(default=datetime.datetime.now)
    salary = fields.DecimalField(max_digits=2, decimal_places=2)
