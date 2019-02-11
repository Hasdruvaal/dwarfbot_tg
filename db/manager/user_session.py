import datetime
import random

from db.manager import SessionManager
from db.models import UserSession


class UserSessionManager:
    def toggle_player(session_id, user_id, force_add=False):
        query = UserSession.select().where((UserSession.session == session_id) &
                                           (UserSession.user == user_id))
        if not query.exists() or force_add:
            position = UserSession \
                           .select() \
                           .where(UserSession.session == session_id) \
                           .order_by(UserSession.position.desc()) \
                           .limit(1)
            if position.exists():
                position = position.get().position
            else:
                position = 0

            UserSession.create(session=session_id, user=user_id, position=position+1)
            return True
        else:
            query.get().delete_instance()
            return False

    def get_players(session_id):
        players = UserSession.select()\
            .where(UserSession.session == session_id)\
            .order_by(UserSession.position)
        current_player = players.filter(UserSession.status)
        current_player = None if not current_player.exists() else current_player.get()

        return {p.position: p.user for p in players}, current_player

    def shuffle_players(curator_id, session):
        user_sessions = SessionManager.get_player_sessions(curator_id)
        session_status = SessionManager.get_session(session).status
        if session.id not in user_sessions or session_status is not None:
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

    def current_user_session(session_id):
        query = UserSession.select().where((UserSession.session == session_id)
                                           & UserSession.status)
        if query.exists():
            return query.get()
        return None

    def next_user_session(session_id):
        cur = UserSessionManager.current_user_session(session_id)
        if not cur:
            return None

        query = UserSession.select().where((UserSession.session == session_id)
                                          & (UserSession.position == cur.position+1))
        if query.exists():
            return query.get()
        return None

    def toggle_status(id):
        user_session = UserSession.get_by_id(id)
        user_session.status = not user_session.status
        user_session.save()
        return user_session.status

    def get_active_sessions(player_id):
        sessions = UserSession.select().where((UserSession.user == player_id)
                                              & UserSession.status)
        return {s.id: s.session.name for s in sessions}

    def get_by_id(user_session_id):
        return UserSession.get_by_id(user_session_id)

    def step(session_id):
        current_user_session = UserSessionManager.current_user_session(session_id)
        next_user_session = UserSessionManager.next_user_session(session_id)
        if current_user_session:
            current_user_session.status = False
            current_user_session.save()
        else:
            return None, None
        if next_user_session:
            next_user_session.status = True
            next_user_session.save()
        return current_user_session, next_user_session

    def round(session_id, shuffle=False):
        round_user_sessions = []
        player_list, cur = UserSessionManager.get_players(session_id)
        if not player_list:
            return False

        for k, user_session in player_list.items():
            round_user_sessions.append(user_session)
        if shuffle:
            random.shuffle(round_user_sessions)
        for user_session in round_user_sessions:
            if not UserSessionManager.toggle_player(session_id = session_id,
                                             user_id = user_session.user,
                                             force_add = True):
                return False
        return True

    def check_save(user_session_id):
        return UserSession.select().where((UserSession.session == user_session_id)
                                                 & (UserSession.game)).exists()

    def write_save(file, user_session_id):
        if not UserSessionManager.check_save(user_session_id):
            user_session = UserSessionManager.get_by_id(user_session_id)
            user_session.game = file
            user_session.save()
            return user_session.game
        else:
            return None

    def get_perv_save(user_session_id):
        if not UserSessionManager.check_save(user_session_id):
            user_session = UserSessionManager.get_by_id(user_session_id)
            prev_session = UserSession.select().where((UserSession.session == user_session.session)
                                                      & (UserSession.position == user_session.position-1))
            return prev_session.get() if prev_session.exists() else None

    def write_perv(user_session_id):
        prev_session = UserSessionManager.get_perv_save(user_session_id)
        if prev_session:
            return UserSessionManager.write_save(prev_session.game, user_session_id)
        return False

    def sleepers():
        query = UserSession.select().where(UserSession.status
                                           & datetime.datetime.now() >= UserSession.date_to)
        if query.exists():
            return query
