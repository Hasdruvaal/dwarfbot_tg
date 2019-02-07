from db.models.user import User
from db.models.session import Session
from db.models.user_session import UserSession

from db.manager.user import UserManager


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
                                       (Session.chatId == chat_id))
        if query.exists():
            query.get().delete_instance()
            return True
        return False

    # returns bool
    def stop_session(curator_id, chat_id):
        curator = User.get(userId=curator_id)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chatId == chat_id) &
                                       Session.active)
        if query.exists():
            session = query.get()
            session.active = False
            return True
        return False

    # returns playerId[]
    def get_players(session_id):
        session = Session.get(sessionId=session_id)
        players = UserSession.select().where(UserSession.session == session).get()
        playerIds = list(map(lambda x: x.userId, players))
        return playerIds

    # returns bool
    def toggle_player(session_id, user_id):
        assert UserManager.check_user(user_id)
        session = Session.get(sessionId=session_id)
        user = User.get(userId=user_id)
        query = UserSession.select().where(
            UserSession.session == session &
            UserSession.user == user)
        if not query.exists():
            UserSession.create(session=session, user=user)
            return True
        else:
            query.get().delete_instance()
            return False

    # returns playerId[]
    def shuffle_players(curator_id, session_id):
        return  # TODO:

    # returns sessionId[]
    def get_chat_sessions(chat_id):
        return  # TODO:

    # returns playerId[]
    def get_player_sessions(player_id):
        return  # TODO:

    # returns Session
    def read_session(session_id):
        return  # TODO:

    # returns bool
    def write_session(session_id):
        return  # TODO:
