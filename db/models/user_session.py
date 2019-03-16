import datetime

from peewee import ForeignKeyField, IntegerField, BooleanField, TextField, DateField
from db import BaseModel
from db.models.user import User
from db.models.session import Session


class UserSession(BaseModel):
    user = ForeignKeyField(User)
    session = ForeignKeyField(Session)
    position = IntegerField(primary_key=False)
    status = BooleanField(default=False)
    game = TextField(null=True)
    date_to = DateField(default=datetime.datetime.now() + datetime.timedelta(days=7))

    def game_name(self):
        return f'{self.position}_{self.session.name}_{self.user.get_name()}.zip'
