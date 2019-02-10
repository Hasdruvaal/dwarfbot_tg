from peewee import SqliteDatabase, Model
from config import telegram

db = SqliteDatabase(telegram.database)


class BaseModel(Model):
    class Meta:
        database = db
