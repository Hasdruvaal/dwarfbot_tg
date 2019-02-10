from db import BaseModel

from db.models.user_session import UserSession
from peewee import ForeignKeyField, BlobField


class Save(BaseModel):
    user_session = ForeignKeyField(UserSession, primary_key=True)
    data = BlobField()

    def get_name(self):
        return '_'.join([str(self.user_session.position), self.user_session.user.get_name()])+'.zip'
