from datetime import datetime
from ..database import db, SCHEMA
from .utils import format_chat_list, format_create_time


class Profile:

    table = 'profile'

    def create(self, data):
        return db.insert(SCHEMA, self.table, data)

    def update(self, data):
        return db.update(SCHEMA, self.table, data)

    def get_by_id(self, id):
        return db.search_by_hash(SCHEMA, self.table, id)[0]

    def get_by_user_id(self, user_id):
        return db.sql(f"SELECT * FROM {SCHEMA}.{self.table} WHERE user_id='{user_id[0]}'")[0]


class Experience:

    table = 'experience'

    def create(self, data):
        return db.insert(SCHEMA, self.table, data)

    def update(self, data):
        return db.update(SCHEMA, self.table, data)

    def get_by_id(self, id):
        return db.search_by_hash(SCHEMA, self.table, id)[0]

    def get_by_user_id(self, user_id, page={'profile':None, 'all':None}):
        experiences = db.sql(f"SELECT * FROM {SCHEMA}.{self.table} WHERE user_id='{user_id[0]}'")
        experiences = sorted(experiences, key=lambda d: datetime.strptime(d['start_date'], '%d-%m-%Y'), reverse=True)
        if 'profile' in page and page['profile'] is not None:
            return experiences[:3]
        elif 'all' in page and page['all'] is not None:
            return experiences


class Chat:

    table = 'chat'

    def create(self, data):
        return db.insert(SCHEMA, self.table, [data])

    def update(self, data):
        return db.update(SCHEMA, self.table, [data])

    def get_user_messages(self, receiver_id, sender_id):
        messages = db.sql(f"SELECT * FROM {SCHEMA}.{self.table} WHERE (receiver_id='{receiver_id}' AND sender_id='{sender_id}') OR (receiver_id='{sender_id}' AND sender_id='{receiver_id}') ORDER BY __createdtime__ ASC")
        return format_create_time(messages, many=True)

    def get_unread_messages(self, receiver_id):
        messages = db.sql(f"SELECT * FROM {SCHEMA}.{self.table} WHERE receiver_id='{receiver_id}' AND status='unread' ORDER BY __createdtime__ ASC")
        return messages, len(messages)

    def get_chats(self, user_id):
        messages = db.sql(f"SELECT * FROM {SCHEMA}.{self.table} WHERE receiver_id='{user_id}' GROUP BY sender_id")
        print(messages)
        return format_chat_list(messages)