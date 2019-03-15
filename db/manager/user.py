from db.manager.base import BaseManager
from db.models import User


class UserManager(BaseManager):
    def add_user(self, **kwargs):
        if not self.get(kwargs.get('id')):
            return self.create(**kwargs)

    def update_user(self, id, user_name, first_name, last_name):
        user = self.get(id)
        if user:
            user.user_name = user_name
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        return user

user_manager = UserManager(User)
