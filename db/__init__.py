from peewee import PostgresqlDatabase, Model
import config


db = PostgresqlDatabase(config.db_name,
                        user=config.db_user,
                        password=config.db_pass,
                        host=config.db_host,
                        port=config.db_port,
                       )


class BaseModel(Model):
    class Meta:
        database = db
