from db import db
from db.models import User, Session, UserSession, Save


def init_db():
    db.create_tables([User, Session, UserSession, Save])
