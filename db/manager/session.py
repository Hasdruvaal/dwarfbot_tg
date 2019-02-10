from db.models.user import User
from db.models import Session, UserSession


class SessionManager:
    # returns sessionId
    def create_session(name, curator_id, chat_id):
        curator = User.get(userId=curator_id)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chatId == chat_id))
        if not query.exists():
            Session.create(name=name, curator=curator, chatId=chat_id)
            return True
        return False

    # returns bool
    def delete_session(curator_id, chat_id):
        curator = User.get(userId=curator_id)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chatId == chat_id) &
                                       (Session.status.is_null()))
        if query.exists():
            query.get().delete_instance()
            return True
        return False

    # returns str or none
    def rename_session(curator_id, chat_id, name):
        curator = User.get_or_none(userId=curator_id)
        query = Session.select().where((Session.chatId == chat_id)
                                       & (Session.status.is_null()
                                          | Session.status))
        if query.exists():
            session = query.get()
            if name and session.curator == curator:
                session.name = name
                session.save()
            return session.name
        return None

    # returns str or none
    def description(curator_id, chat_id, description):
        curator = User.get_or_none(userId=curator_id)
        query = Session.select().where((Session.chatId == chat_id)
                                       & (Session.status.is_null()
                                          | Session.status))
        if query.exists():
            session = query.get()
            if description and session.curator == curator:
                session.description = description
                session.save()
            return session.description
        return None

    # returns sessionId
    def get_session(chat_id):
        query = Session.select().where((Session.chatId == chat_id))
        if query.exists():
            session = query.get()
            return session.sessionId
        return None

    # returns sessionId[]
    def get_player_sessions(curator_id):
        sessions = Session.select()\
            .where((Session.curator == curator_id))
        return [session.sessionId for session in sessions]

    # returns sessionId[]
    def get_session_status(sesion_id):
        session = Session.get(sesion_id)
        return session.status

    # return bool
    def start_session(session_id, curator_id):
        players = UserSession.select().where(UserSession.session == session_id)
        if players.exists():
            session = Session.get(session_id)
            session.status = True
            session.save()
            return True
        return False

    # returns Session
    def read_session(session_id):
        return  # TODO:

    # returns bool
    def write_session(session_id):
        return  # TODO:
