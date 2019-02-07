from peewee import SqliteDatabase, Model
from config import bot

db = SqliteDatabase(bot.database)


class BaseModel(Model):
    class Meta:
        database = db
