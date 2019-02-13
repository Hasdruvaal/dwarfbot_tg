import datetime

from peewee import ForeignKeyField, IntegerField, BooleanField, TextField, DateField
from db.models import BaseModel
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
        return '{}_{}_{}.zip'.format(self.position, self.session.name, self.user.get_name())
