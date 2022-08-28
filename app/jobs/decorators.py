from functools import wraps
from .service import JobService
from flask import session, redirect, url_for


def job_owner_required(view_func):
    @wraps(view_func)
    def wrapper_func(*args, **kwargs):
        job = JobService().get_job(kwargs['id'])
        if job[0]['owner'] == session['user']['id']:
            return view_func(*args, **kwargs)
        else:
            return redirect(url_for('auth.index'))
    return wrapper_func