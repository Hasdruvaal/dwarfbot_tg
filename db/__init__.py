from peewee import PostgresqlDatabase, SqliteDatabase, Model
import config

if config.dev_mode:
    db = SqliteDatabase(f'{config.db_name}.db')
else:
    db = PostgresqlDatabase(config.db_name,
                            user=config.db_user,
                            password=config.db_pass,
                            host=config.db_host,
                            port=config.db_port,
                            )


class BaseModel(Model):
    class Meta:
        database = db
