from db.manager.base import BaseManager
from db.models import User


class UserManager(BaseManager):
    def add_user(self, **kwargs):
        if not self.get(kwargs.get('id')):
            return self.create(**kwargs)


userManager = UserManager(User)
