from .models import Profile, Experience, Chat


class ProfileService:

    model_name = Profile

    def __init__(self):
        self.model = self.model_name()

    def create(self, data):
        return self.model.create([data])

    def update(self, id, data):

        data['id'] = id
        
        return self.model.update([data])

    def get_by_id(self, id):
        return self.model.get_by_id([id])

    def get_by_user_id(self, user_id):
        return self.model.get_by_user_id([user_id])

    def get_skills_by_user_id(self, user_id):
        profile = self.get_by_user_id(user_id)
        return profile['skills']


class ExperienceService:

    model_name = Experience

    def __init__(self):
        self.model = self.model_name()

    def create(self, data):
        return self.model.create([data])

    def update(self, id, data):

        data['id'] = id
        
        return self.model.update([data])

    def get_by_id(self, id):
        return self.model.get_by_id([id])

    def get_by_user_id(self, user_id, page):
        return self.model.get_by_user_id([user_id], page)


class ChatService:

    model_name = Chat

    def __init__(self):
        self.model = self.model_name()

    def create(self, data):
        return self.model.create(data)
    
    def update(self, id, data):

        data['id'] = id
        
        return self.model.update(data)

    def get_user_messages(self, receiver_id, sender_id):
        return self.model.get_user_messages(receiver_id, sender_id)

    def get_unread_messages(self, receiver_id):
        return self.model.get_unread_messages(receiver_id)

    def get_chats(self, user_id):
        return self.model.get_chats(user_id)