from db import BaseModel
from peewee import IntegerField


class User(BaseModel):
    userId = IntegerField(primary_key=True)
    pmId = IntegerField()
