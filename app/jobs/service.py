from .models import Job


class JobService:

    model_name = Job

    def __init__(self):
        self.model = self.model_name()

    def create_job(self, job_list):
        return self.model.create(job_list)

    def get_job(self, id):
        return self.model.get(id)