from flask import render_template, session, redirect, url_for, flash, request
from . import auth
from .decorators import developer_required, login_required, unauthenticated_user, hiring_manager_required
from .forms import LoginForm, RegisterForm, SearchForm
from ..extensions import bcrypt
from .service import UserService
from app.user.service import ProfileService


@auth.route('/', defaults={'skill': None}, methods=['GET', 'POST'])
@auth.route('/<string:skill>', methods=['GET', 'POST'])
@login_required
def index(skill=None):
    form = SearchForm()
    users = []
    search_term = ''
    result_count = 0
    if form.validate_on_submit():
        category = form.category.data
        search_term = form.q.data
        if category == 'dev':
            users = UserService.search(search_term)
            for user in users:
                user['profile'] = ProfileService().get_by_user_id(user['id'])
    elif skill:
        search_term = skill
        users = UserService.search(search_term)
        for user in users:
            user['profile'] = ProfileService().get_by_user_id(user['id'])
    result_count = len(users)
    return render_template('index.html', home=True, form=form, users=users, search_term=search_term, result_count=result_count)


@auth.route('/register/', methods=['GET', 'POST'])
@unauthenticated_user
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = {
            'full_name': form.full_name.data,
            'username': form.username.data,
            'email': form.email.data,
            'hashed_password': bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            'role': form.role.data
        }
        created_user = UserService().create_user(user)
        ProfileService().create({'user_id':created_user['inserted_hashes'][0], 'skills':[]})
        flash(
            f"Account for {user['username']} created successfully!", 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login/', methods=['GET', 'POST'])
@unauthenticated_user
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserService().get_user_by_attr('email', form.email.data)
        print(user)
        if user and bcrypt.check_password_hash(user[0]['hashed_password'], form.password.data):
            session['user'] = user[0]
            flash(f"Welcome, {session['user']['username']}", 'success')
            return redirect(url_for('auth.index'))
        else:
            flash('Please check your credentials.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    session.pop('user')
    return redirect(url_for('auth.login'))
