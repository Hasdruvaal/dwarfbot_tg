from db.models.user import User


class UserManager:
    # returns bool
    def check_user(user_id):
        return User.select().where(User.user == user_id).exists()

    # returns bool
    def add_user(user_id, chat_id, username, first_name, last_name):
        if not UserManager.check_user(user_id):
            User.create(user=user_id,
                        user_name=username,
                        first_name=first_name,
                        last_name=last_name)
            return True
        return False
