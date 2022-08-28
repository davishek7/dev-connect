from dataclasses import dataclass
from datetime import datetime
from flask import session
from app.user.service import ChatService, ProfileService


def common_context():

    now = datetime.now()
    current_user = session['user'] if 'user' in session else None
    add_skill = False
    unread_msg_count = ChatService().get_unread_messages(session['user']['id'])[1] if 'user' in session else None
    profile = ProfileService().get_by_user_id(session['user']['id']) if 'user' in session else None
    if profile and 'skills' in profile and len(profile.get('skills', [])) == 0:
        add_skill = True
    return {
        'now': now,
        'current_user': current_user,
        'unread_msg_count': unread_msg_count,
        'add_skill': add_skill,
        'github_url': 'https://www.github.com/davishek7',
        'twitter_url': 'https://twitter.com/davishek7',
        'linkedin_url': 'https://www.linkedin.com/in/davishek7/'
    }
