from db.models.user import User
from db.models.session import Session


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
                                       (Session.active.is_null()))
        if query.exists():
            query.get().delete_instance()
            return True
        return False

    # returns bool
    def rename_session(name, curator_id, chat_id):
        curator = User.get(userId=curator_id)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chatId == chat_id))
        if query.exists():
            session = query.get()
            session.name = name
            session.save()
            return True
        return False

    # returns bool
    def change_status_session(curator_id, chat_id, status=False):
        curator = User.get(userId=curator_id)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chatId == chat_id))
        if query.exists():
            session = query.get()
            session.active = status
            session.save()
            return True
        return False

    #returns str or none
    def description(curator_id, chat_id, description):
        curator = User.get(userId=curator_id)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chatId == chat_id))
        if query.exists():
            session = query.get()
            if description:
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

    # returns Session
    def read_session(session_id):
        return  # TODO:

    # returns bool
    def write_session(session_id):
        return  # TODO:
