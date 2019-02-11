from db import BaseModel
from peewee import IntegerField, TextField


class User(BaseModel):
    user = IntegerField(primary_key=True)
    user_name = TextField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)

    def get_name(self):
        return self.user_name or self.first_name+' '+self.last_name
