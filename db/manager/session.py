from db.manager.base import BaseManager
from db.manager.user import userManager
from db.models import Session
from db.models import UserSession


class SessionManager(BaseManager):
    def create_session(self, name, curator_id, chat_id):
        query = self.select().where((self.model.chat == chat_id)
                                    & (self.model.status.is_null() | self.model.status))
        if not query.exists():
            return self.create(name=name, curator=userManager.get(curator_id), chat=chat_id)

    def delete_session(self, curator_id, chat_id):
        session = self.active_chat_session(chat_id)
        if session and session.curator_id == str(curator_id):
            UserSession.delete().where((UserSession.session == session)).execute()
            return self.delete().where((self.model.curator == curator_id) &
                                       (self.model.chat == chat_id) &
                                       (self.model.status.is_null())) \
                                .execute()

    def active_chat_session(self, chat_id):
        query = self.select().where((self.model.chat == chat_id)
                                    & (self.model.status.is_null()
                                       | self.model.status))
        if query.exists():
            return query.get()

    def rename(self, curator_id, chat_id, name=''):
        session = self.active_chat_session(chat_id)
        if session:
            if name and session.curator == userManager.get(curator_id):
                session.name = name
                session.save()
            return session.name

    def description(self, curator_id, chat_id, description=''):
        session = self.active_chat_session(chat_id)
        if session:
            if description and session.curator == userManager.get(curator_id):
                session.description = description
                session.save()
            return session.description

    def get_player_sessions(self, curator_id):
        sessions = self.select().where(self.model.curator == userManager.get(curator_id))
        return [session.id for session in sessions]

    def start(self, session_id):
        player_session = UserSession.select().where(UserSession.session == session_id) \
                                             .order_by(UserSession.position)
        if player_session.exists():
            session = self.get(session_id)
            session.status = True
            session.save()
            session.init_cloud()
            session.create_album()
            player_session = player_session.get()
            player_session.status = True
            return player_session.save()
        return False

    def stop(self, session_id):
        player_session = UserSession.select().where((UserSession.session == session_id)
                                                    & UserSession.status)
        if player_session.exists():
            player_session = player_session.get()
            player_session.status = False
            player_session.save()
        session = self.get(session_id)
        if session.status == True:
            session.status = False
            return session.save()


sessionManager = SessionManager(Session)
