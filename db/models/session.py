from peewee import IntegerField, TextField, ForeignKeyField, BooleanField
from db.models import BaseModel
from db.models.user import User


class Session(BaseModel):
    sessionId = IntegerField(primary_key=True)
    name = TextField()
    curator = ForeignKeyField(User)
    chatId = IntegerField()
    active = BooleanField(null=True)
    description = TextField(null=True)

