from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(view_func):
    @wraps(view_func)
    def wrapper_func(*args, **kwargs):
        if 'user' in session:
            return view_func(*args, **kwargs)
        else:
            flash('You are not authorised, Please login first.', 'warning')
            return redirect(url_for('auth.login'))
    return wrapper_func

def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper_func(*args, **kwargs):
        if 'user' not in session:
            return view_func(*args, **kwargs)
        else:
            flash('You are not authorised', 'warning')
            return redirect(url_for('auth.index'))
    return wrapper_func

def hiring_manager_required(view_func):
    @wraps(view_func)
    def wrapper_func(*args, **kwargs):
        if session['user']['role'] == 'Hiring Manager':
            return view_func(*args, **kwargs)
        else:
            # flash('You are not authorised.', 'warning')
            return redirect(url_for('auth.index'))
    return wrapper_func

def developer_required(view_func):
    @wraps(view_func)
    def wrapper_func(*args, **kwargs):
        if session['user']['role'] == 'Developer':
            return view_func(*args, **kwargs)
        else:
            # flash('You are not authorised.', 'warning')
            return redirect(request.referrer)
    return wrapper_func