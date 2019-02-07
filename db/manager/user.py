from db.models.user import User


class UserManager:
    # returns bool
    def check_user(user_id):
        return User.select().where(User.userId == user_id).exists()

    # returns bool
    def add_user(user_id, chat_id):
        if not UserManager.check_user(user_id):
            User.create(userId=user_id, pmId=chat_id)
            return True
        return False
