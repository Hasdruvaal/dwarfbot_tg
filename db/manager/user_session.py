import datetime
import random

from db.manager.base import BaseManager
from db.manager.session import sessionManager
from db.models import UserSession


class UserSessionManager(BaseManager):
    def by_session(self, session_id, reverse=False):
        ordering = self.model.position.desc() if reverse else self.model.position
        return self.select().where(self.model.session == session_id) \
            .order_by(ordering)

    def toggle_player(self, session_id, user_id, force_add=False):
        query = self.select().where((self.model.session == session_id) &
                                    (self.model.user == user_id))
        if not query.exists() or force_add:
            position = self.by_session(session_id, True).limit(1)
            position = position.get().position if position.exists() else 0
            return self.create(session=session_id, user=user_id, position=position + 1)
        else:
            return query.get().delete_instance()

    def active_player(self, session_id):
        query = self.select().where((self.model.session == session_id)
                                    & self.model.status)
        return query.get() if query.exists() else None

    def all_player_active(self, player_id):
        sessions = self.select().where((self.model.user == player_id)
                                       & self.model.status)
        return {s.id: s.session.name for s in sessions}

    def next_or_prev(self, session_id, previous=False):
        current = self.active_player(session_id)
        if current:
            position = current.position - 1 if previous else current.position + 1
            query = self.model.select().where((self.model.session == session_id)
                                              & (self.model.position == position))
            return query.get() if query.exists() else None

    def get_players(self, session_id):
        players = self.by_session(session_id)
        current_player = self.active_player(session_id)
        return {p.position: p.user for p in players}, current_player

    def shuffle_players(self, session):
        session_status = sessionManager.get(session).status
        if session_status is None:
            query = self.by_session(session)
            if query.exists():
                players = [player.id for player in query]
                random.shuffle(players.reverse())
                for player in players:
                    user_session = self.get(player)
                    user_session.position = players.index(player) + 1
                    user_session.save()
                return True

    def step(self, session_id):
        current = self.active_player(session_id)
        next_session = self.next_or_prev(session_id)
        if current:
            current.status = False
            current.save()
        else:
            return None, None
        if next_session:
            next_session.status = True
            next_session.save()
        return current, next_session

    def round(self, session_id, shuffle=False):
        round_user_sessions = []
        player_list, cur = self.get_players(session_id)
        if player_list:
            for k, user_session in player_list.items():
                round_user_sessions.append(user_session)
            if shuffle:
                random.shuffle(round_user_sessions)
            for user_session in round_user_sessions:
                self.toggle_player(session_id=session_id,
                                   user_id=user_session.id,
                                   force_add=True)
            return True

    def check_save(self, user_session_id):
        return self.select().where((self.model.session == user_session_id)
                                   & self.model.game).exists()

    def write_save(self, file_id, user_session_id):
        if not self.check_save(user_session_id):
            user_session = self.get(user_session_id)
            user_session.game = file_id
            user_session.save()
            return user_session.game
        else:
            return None

    def write_from_prev(self, user_session_id):
        session_id = self.get(user_session_id)
        previous = self.next_or_prev(session_id, True)
        if previous and previous.game:
            return self.write_save(previous.game, user_session_id)

    def sleepers(self):
        now = datetime.datetime.now()
        query = self.select().where(self.model.status
                                    & ((self.model.date_to.year < now.year)
                                       | (self.model.date_to.month < now.month)
                                       | (self.model.date_to.day < now.day)))
        return query if query.exists() else None


userSessionManager = UserSessionManager(UserSession)
