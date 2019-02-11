from db.models import Save
from db.manager import UserSessionManager


class SaveManager:
    def check_save(user_session_id):
        return Save.select().where(Save.user_session == user_session_id).exists()

    def write_save(file, user_session_id):
        if not SaveManager.check_save(user_session_id):
            Save.create(data=file,
                        user_session=user_session_id)
            UserSessionManager.step(UserSessionManager.get_by_id(user_session_id).session_id)
        else:
            return None

    def get_save(user_session_id):
        save = Save.select().where(Save.user_session == user_session_id).get()
        return {'name': save.get_name(),
                'data': save.data}
