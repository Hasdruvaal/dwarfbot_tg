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
                           .limit(1)[0].position or 1

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
    def shuffle_players(curator_id, session_id):
        sessions = SessionManager.get_player_sessions(curator_id)
        if session_id not in sessions:
            return None
        query = UserSession.select().where((UserSession.session_id == session_id))
        if query.exists():
            players = [player.user for player in query]
            random.shuffle(players)
            for player in players:
                user_session = UserSession.select().where((UserSession.session == session_id)
                                                         & (UserSession.user == player)).get()
                user_session.position = players.index(player)
                user_session.save()
            return True
        return None
