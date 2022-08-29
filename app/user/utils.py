from datetime import datetime
from flask import session
from ..database import db, SCHEMA


def format_create_time(data, many=False):

    if many:
        for _ in range(len(data)):
            data[_]['__createdtime__'] = datetime.fromtimestamp(data[_]['__createdtime__']/1000).strftime('%d-%m-%Y %I:%M %p')
        return data
    else:
        data['__createdtime__'] = datetime.fromtimestamp(data['__createdtime__']/1000).strftime('%d-%m-%Y %I:%M %p')
        return data

def format_chat_list(data):

    _data = {}
    chats = []

    for _ in range(len(data)):
        # _data['id'] = data[_]['id']
        _data['sender'] = db.search_by_hash(SCHEMA, 'user', [data[_]['sender_id']])[0]['username']
        _data['last_message'] = db.sql(f"SELECT message, status, __createdtime__ FROM {SCHEMA}.chat WHERE (receiver_id='{data[_]['receiver_id']}' AND sender_id='{data[_]['sender_id']}') OR (receiver_id='{data[_]['sender_id']}' AND sender_id='{data[_]['receiver_id']}') ORDER BY __createdtime__ DESC")[0]

        if _data not in chats:
            chats.append(_data)
    print(chats)
    return chats