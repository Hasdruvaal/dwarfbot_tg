class BaseManager:
    def __init__(self, model):
        self.model = model

    def get(self, pkey):
        query = self.select().where(self.model.id == pkey)
        return query.get() if query.exists() else None

    def create(self, **kwargs):
        return self.model.create(**kwargs)

    def delete(self, *args, **kwargs):
        return self.model.delete(*args, **kwargs)

    def select(self, *args, **kwargs):
        return self.model.select(*args, **kwargs)
