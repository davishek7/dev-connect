from functools import wraps
from .service import ExperienceService
from flask import session, redirect, url_for, request

def edit_permission_required(view_func):
    @wraps(view_func)
    def wrapper_func(*args, **kwargs):
        exp = ExperienceService().get_by_id(kwargs['id'])
        if exp['user_id'] == session['user']['id']:
            return view_func(*args, **kwargs)
        else:
            return redirect(request.referrer)
    return wrapper_func

# def profile_user_required(view_func)