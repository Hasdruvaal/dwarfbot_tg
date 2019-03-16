from db import BaseModel
from peewee import TextField


class User(BaseModel):
    id = TextField(primary_key=True)
    user_name = TextField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)

    def get_name(self):
        name_alias = '{} {}'.format(self.first_name or '', self.last_name or '')
        return self.user_name or name_alias.strip() or str(id)
