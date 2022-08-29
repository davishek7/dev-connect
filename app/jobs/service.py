from .models import Job


class JobService:

    model_name = Job

    def __init__(self):
        self.model = self.model_name()

    def create(self, data):
        return self.model.create([data])

    def update(self, id, data):
        data['id'] = id
        return self.model.update([data])

    def get_job(self, id):
        return self.model.get(id)

    @classmethod
    def search(cls, value):
        return cls.model_name.search(value)

    @classmethod
    def get_all(cls):
        return cls.model_name.get_all()
    
    def apply(self, id, user_id):
        job = self.get_job(id)
        job['applicants'].append(user_id)
        return self.update(id, job)