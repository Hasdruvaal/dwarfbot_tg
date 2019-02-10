from db import BaseModel
from peewee import IntegerField, TextField


class User(BaseModel):
    userId = IntegerField(primary_key=True)
    pmId = IntegerField()
    userName = TextField(null=True)
    firstName = TextField(null=True)
    lastName = TextField(null=True)

    def get_name(self):
        return self.userName or self.firstName+' '+self.lastName
