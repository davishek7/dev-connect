from ..database import db, SCHEMA

class Job:

    table = 'job'

    def create(self, job_list):
        return db.insert(SCHEMA, self.table, job_list)

    def update(self, job_list):
        return db.update(SCHEMA, self.table, job_list)

    def delete(self, id):
        return db.delete(SCHEMA, self.table, [id])

    def get(self, id):
        return db.search_by_hash(SCHEMA, self.table, [id], get_attributes=['*'])

    @classmethod
    def get_user_by_attr(cls, attribute, value):
        return db.search_by_value(SCHEMA, cls.table, attribute, value)

    @classmethod
    def search(cls, value):
        users = cls.get_all()
        results = [user for user in users if user['skills'] is not None and value in user['skills']]
        return results

    @classmethod
    def get_all(cls):
        return db.sql(f'SELECT id, email, username, role, skills, __createdtime__, __updatedtime__ FROM {SCHEMA}.{cls.table}')

