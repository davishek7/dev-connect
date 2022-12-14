from flask import render_template, session, redirect, url_for, flash, request
from . import auth
from .decorators import developer_required, login_required, unauthenticated_user, hiring_manager_required
from .forms import LoginForm, RegisterForm, SearchForm
from ..extensions import bcrypt
from .service import UserService
from app.user.service import ProfileService
from app.jobs.service import JobService


@auth.route('/', defaults={'skill': None}, methods=['GET', 'POST'])
@auth.route('/<string:skill>', methods=['GET', 'POST'])
@login_required
def index(skill=None):
    form = SearchForm()
    users = []
    jobs = []
    search_term = ''
    result_count = 0
    if form.validate_on_submit():
        category = form.category.data
        search_term = form.q.data
        if category == 'dev':
            users = UserService.search(search_term)
            for user in users:
                user['profile'] = ProfileService().get_by_user_id(user['id'])
            result_count = len(users)
        if category == 'job':
            jobs = JobService.search(search_term)
            result_count = len(jobs)
    elif skill:
        search_term = skill
        users = UserService.search(search_term)
        for user in users:
            user['profile'] = ProfileService().get_by_user_id(user['id'])
    return render_template('index.html', home=True, form=form, users=users, jobs=jobs, search_term=search_term, result_count=result_count)


@auth.route('/register/', methods=['GET', 'POST'])
@unauthenticated_user
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = {
            'full_name': form.first_name.data + form.last_name.data,
            'username': form.username.data,
            'email': form.email.data,
            'hashed_password': bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            'role': form.role.data,
            'bookmarks': []
        }
        created_user = UserService().create_user(user)
        ProfileService().create({'user_id':created_user['inserted_hashes'][0], 'skills':[]})
        flash(
            f"Account for {user['username']} created successfully!", 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, register=True)


@auth.route('/login/', methods=['GET', 'POST'])
@unauthenticated_user
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserService().get_user_by_attr('email', form.email.data)
        if user and bcrypt.check_password_hash(user[0]['hashed_password'], form.password.data):
            session['user'] = user[0]
            flash(f"Welcome, {session['user']['username']}", 'success')
            return redirect(url_for('auth.index'))
        else:
            flash('Please check your credentials.', 'danger')
    return render_template('auth/login.html', form=form, login=True)


@auth.route('/logout/')
@login_required
def logout():
    session.pop('user')
    return redirect(url_for('auth.login'))
