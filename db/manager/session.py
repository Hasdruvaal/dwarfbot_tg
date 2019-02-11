from peewee import fn
import random

from db.models.user import User
from db.models import Session, UserSession


class SessionManager:
    def create_session(name, curator_id, chat_id):
        curator = User.get(user=curator_id)
        query = Session.select().where((Session.chat == chat_id)
                                        & Session.status is not False) # can be null!
        if not query.exists():
            Session.create(name=name, curator=curator, chat=chat_id)
            return True
        return False

    def delete_session(curator_id, chat_id):
        curator = User.get(user=curator_id)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chat == chat_id) &
                                       (Session.status.is_null()))
        if query.exists():
            query.get().delete_instance()
            return True
        return False

    def rename_session(curator_id, chat_id, name):
        curator = User.get_or_none(user=curator_id)
        query = Session.select().where((Session.chat == chat_id)
                                       & (Session.status.is_null()
                                          | Session.status))
        if query.exists():
            session = query.get()
            if name and session.curator == curator:
                session.name = name
                session.save()
            return session.name
        return None

    def description(curator_id, chat_id, description):
        curator = User.get_or_none(user=curator_id)
        query = Session.select().where((Session.chat == chat_id)
                                       & (Session.status.is_null()
                                          | Session.status))
        if query.exists():
            session = query.get()
            if description and session.curator == curator:
                session.description = description
                session.save()
            return session.description
        return None

    def get_chat_session(chat_id):
        query = Session.select().where((Session.chat == chat_id))
        if query.exists():
            session = query.get()
            return session
        return None

    def get_session(session_id):
        return Session.get_by_id(session_id)


    def get_player_sessions(curator_id):
        sessions = Session.select()\
            .where((Session.curator == curator_id))
        return [session.id for session in sessions]

    def start_session(session_id):
        player_session = UserSession.select()\
            .where(UserSession.session == session_id)\
            .order_by(UserSession.position)
        if player_session.exists():
            session = Session.get_by_id(session_id)
            session.status = True
            session.save()
            player_session = player_session.get()
            player_session.status = True
            player_session.save()
            return True
        return False

    def stop_session(session_id):
        player_session = UserSession.select()\
            .where((UserSession.session == session_id)
                   & (UserSession.status))
        if player_session.exists():
            player_session = player_session.get()
            player_session.status = False
            player_session.save()
        session = Session.get_by_id(session_id)
        session.status = False
        return session.save()
