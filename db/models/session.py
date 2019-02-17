import re
from peewee import AutoField, TextField, ForeignKeyField, BooleanField

from db.models import BaseModel
from db.models.user import User

import images
from cloud import googleDrive


class Session(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField()
    curator = ForeignKeyField(User)
    chat = TextField()
    status = BooleanField(null=True)
    description = TextField(null=True)
    document = TextField(null=True)
    folder = TextField(null=True)
    album = TextField(null=True)

    def hashtag(self):
        hashtag = self.name.replace(' ', '_')
        regex = re.compile('[^a-z_A-Z]')
        return '#'+regex.sub('', hashtag)

    def create_album(self):
        params = { 'title': self.name,
                   'description': self.description }
        album = images.client.create_album(params)
        self.album = album.get('id')
        return self.save()

    def init_cloud(self):
        self.folder = googleDrive.create_folder(self.name)
        self.document = googleDrive.create_doc(self.name, self.folder)
        return self.save()
