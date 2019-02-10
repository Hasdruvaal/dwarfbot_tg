from peewee import fn
import random

from db.manager import SessionManager
from db.models import UserSession


class UserSessionManager:
    # returns bool
    def toggle_player(session_id, user_id):
        query = UserSession.select().where((UserSession.session == session_id) &
                                           (UserSession.user == user_id))
        if not query.exists():
            position = UserSession \
                           .select(fn.Max(UserSession.position)) \
                           .where(UserSession.session == session_id) \
                           .limit(1).get().position or 1

            UserSession.create(session=session_id, user=user_id, position=position)
            return True
        else:
            query.get().delete_instance()
            return False

    # returns playerId[]
    def get_players(session_id):
        players = UserSession.select()\
            .where(UserSession.session == session_id)\
            .order_by(UserSession.position)
        return {p.position: p.user.get_name() for p in players}

    # returns bool
    def shuffle_players(curator_id, session):
        sessions = SessionManager.get_player_sessions(curator_id)
        session_status = SessionManager.get_session(session).status
        if session.sessionId not in sessions or session_status is not None:
            return None
        query = UserSession.select().where((UserSession.session == session))
        if query.exists():
            players = [player.user for player in query]
            random.shuffle(players)
            for player in players:
                user_session = UserSession.select().where((UserSession.session == session)
                                                         & (UserSession.user == player)).get()
                user_session.position = players.index(player) + 1
                user_session.save()
            return True
        return None

    # return playerId
    def current_user_session(session_id):
        user_session = UserSession.select().where((UserSession.session == session_id)
                                                  & UserSession.status)
        if user_session.exists():
            return user_session.get()
        return None

    # return status
    def toggle_status(id):
        user_session = UserSession.get_by_id(id)
        user_session.status = not user_session.status
        user_session.save()
        return user_session.status

    # return session{id:name}
    def get_active_sessions(player_id):
        sessions = UserSession.select().where((UserSession.user == player_id)
                                              & UserSession.status)
        return {s.id: s.session.name for s in sessions}

    def get_by_id(user_session_id):
        return UserSession.get_by_id(user_session_id)

    def step(session_id):
        user_session = UserSessionManager.current_user_session(session_id)
        if user_session:
            user_session.status = False
            user_session.save()
        else:
            return False

        user_session = UserSession.select().where((UserSession.session_id == session_id)
                                                  & (UserSession.position == user_session.position+1))
        if user_session.exists():
            user_session = user_session.get()
            user_session.status = True
            user_session.save()
        return True
