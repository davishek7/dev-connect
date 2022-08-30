from ..database import db, SCHEMA
from flask import session

class User:

    table = 'user'

    def create(self, user_list):
        return db.insert(SCHEMA, self.table, user_list)

    def update(self, user_list):
        return db.update(SCHEMA, self.table, user_list)

    @classmethod
    def get_user_by_attr(cls, attribute, value):
        return db.search_by_value(SCHEMA, cls.table, attribute, value)

    def get(self, id):
        return db.search_by_hash(SCHEMA, self.table, [id], get_attributes=['*'])

    @classmethod
    def search(cls, value):
        users = cls.get_all()
        users = list(filter(lambda d : d['id'] != session['user']['id'], users))
        results = []
        values = value.split(',')
        print(values)
        for user in users:
            profile = db.search_by_value(SCHEMA, 'profile', 'user_id', [user['id']])[0]
            if profile:
                for skill in profile['skills']:
                    for _value in values:
                        if _value.lower().strip() in skill.lower() and user not in results:
                            results.append(user)
        return results


    @classmethod
    def get_all(cls):
        return db.sql(f'SELECT * FROM {SCHEMA}.{cls.table}')