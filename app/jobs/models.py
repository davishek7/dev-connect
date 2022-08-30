from ..database import db, SCHEMA
from flask import session
from app.user.utils import format_create_time

class Job:

    table = 'job'

    def create(self, data):
        return db.insert(SCHEMA, self.table, data)

    def update(self, data):
        return db.update(SCHEMA, self.table, data)

    def delete(self, id):
        return db.delete(SCHEMA, self.table, [id])

    def get(self, id):
        job = db.search_by_hash(SCHEMA, self.table, [id], get_attributes=['*'])[0]
        return format_create_time(job)

    @classmethod
    def get_user_by_attr(cls, attribute, value):
        return db.search_by_value(SCHEMA, cls.table, attribute, value)

    @classmethod
    def search(cls, value):
        jobs = cls.get_all()
        values = value.split(',')
        print(values)
        jobs = list(filter(lambda d : d['owner'] != session['user']['id'], jobs))
        results = []
        for job in jobs:
            for skill in job['skills']:
                for _value in values:
                    if _value.lower().strip() in skill.lower() and job not in results:
                        results.append(job)
        return results

    @classmethod
    def get_all(cls):
        jobs = db.sql(f'SELECT id, title, company, emp_type, owner, job_type, location, description, skills, __createdtime__, __updatedtime__ FROM {SCHEMA}.{cls.table} ORDER BY __createdtime__')
        return format_create_time(jobs, many=True)