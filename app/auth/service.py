from .models import User


class UserService:

    model_name = User
    
    def __init__(self):
        self.model = self.model_name()

    def create_user(self, params):
        return self.model.create([params])

    def update_user(self, user_id, params):
        if isinstance(params, dict):
            params = [params]

        for param in params:
            param["id"] = user_id
        
        return self.model.update(params)

    def get_user(self, id):
        return self.model.get(id)
    
    @classmethod
    def get_user_by_attr(cls, attribute, value):
        return cls.model_name.get_user_by_attr(attribute, value)

    @classmethod
    def search(cls, value):
        return cls.model_name.search(value)

    @classmethod
    def get_all(cls):
        return cls.model_name.get_all()

    def bookmark(self, id, job_id):
        user = self.get_user(id)[0]
        action = 'add'
        if 'bookmarks' not in user:
            user['bookmarks'] = []
        if job_id not in user['bookmarks']:
            user['bookmarks'].append(job_id)
        else:
            user['bookmarks'].remove(job_id)
            action = 'remove'
        self.update_user(id, user)
        return user['bookmarks'], action