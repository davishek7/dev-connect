from crypt import methods
from flask import render_template, flash, url_for, session, redirect, request
from . import user
from app.auth.service import UserService
from app.auth.decorators import login_required, developer_required
from .forms import ProfileForm, ExperienceForm, ChatForm
from .service import ExperienceService, ProfileService, ChatService
from .decorators import edit_permission_required
from datetime import datetime


@user.route('/profile/<string:username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = UserService.get_user_by_attr('username', username)[0]
    profile = ProfileService().get_by_user_id(user['id'])
    experience = []
    form = ProfileForm()
    e_form = ExperienceForm()
    c_form = ChatForm()
    messages = []
    if form.validate_on_submit():
        user_data = {'email':form.email.data, 'username':form.username.data, 'full_name':form.full_name.data}
        UserService().update_user(user['id'], [{'email':form.email.data, 'username':form.username.data, 'full_name':form.full_name.data}])
        ProfileService().update(profile['id'], {'skills':form.skills.data, 'bio':form.bio.data, 'status':form.status.data})
        if user_data['username'] != session['user']['username']:
            flash('Profile updated, please login again.', 'info')
            session.pop('user')
            return redirect(url_for('auth.login'))
        else:
            flash('Profile updated successfully.', 'success')
            return redirect(url_for('user.profile', username=username))
    if request.method == 'GET':
        form.full_name.data = user['full_name']
        form.username.data = user['username']
        form.email.data = user['email']
        form.skills.data = profile['skills'] if 'skills' in profile else None
        form.bio.data = profile['bio'] if 'bio' in profile else None
        form.status.data = profile['status'] if 'status' in profile else None
        experience = ExperienceService().get_by_user_id(
            user['id'], {'profile': True})
        if user['id'] != session['user']['id']:
            messages = ChatService().get_user_messages(user['id'], session['user']['id'])
            for _ in range(len(messages)):
                if messages[_]['receiver_id'] == session['user']['id']:
                    ChatService().update(messages[_]['id'], {'status':'read'})
    return render_template('user/profile.html', user=user, user_profile=profile, form=form, e_form=e_form, experience=experience, profile=True, messages=messages, c_form=c_form)

@user.route('/add-experience', methods=['POST'])
@login_required
@developer_required
def add_experience():
    if request.method == 'POST':
        form = ExperienceForm()
        if form.validate_on_submit():
            experience = {
                'title': form.title.data,
                'organization': form.organization.data,
                'start_date': (form.start_date.data).strftime('%d-%m-%Y'),
                'end_date': (form.end_date.data).strftime('%d-%m-%Y'),
                'current': form.current.data,
                'user_id': session['user']['id']
            }
            ExperienceService().create(experience)
            flash('Experience added successfully', 'success')
            return redirect(request.referrer)
        else:
            if form.errors:
                for error, msg in form.errors.items():
                    flash(msg[0], 'warning')
            return redirect(request.referrer)

@user.route('/experiences/<string:user_id>')
@login_required
@developer_required
def experiences(user_id):
    user = UserService().get_user(user_id)[0]
    experience = ExperienceService().get_by_user_id(user_id, {'all':True})
    form = ExperienceForm()
    return render_template('user/experiences.html', experience=experience, user=user, e_form=form)

@user.route('edit-experience/<string:id>', methods=['GET', 'POST'])
@login_required
@developer_required
@edit_permission_required
def edit_experience(id):
    exp = ExperienceService().get_by_id(id)
    form = ExperienceForm()
    if form.validate_on_submit():
        ExperienceService().update(id, {'title':form.title.data, 'organization':form.organization.data, 
                                        'start_date': (form.start_date.data).strftime('%d-%m-%Y'),
                                        'end_date': (form.end_date.data).strftime('%d-%m-%Y') if form.end_date.data is not None else None, 'current': form.current.data})
        flash('Experience updated successfully.', 'success')
        return redirect(url_for('user.experiences', user_id=exp['user_id']))
    if request.method == 'GET':
        form.title.data = exp['title']
        form.organization.data = exp['organization']
        form.start_date.data = datetime.strptime(exp['start_date'], '%d-%m-%Y')
        form.end_date.data = datetime.strptime(exp['end_date'], '%d-%m-%Y') if exp['end_date'] is not None else None
        form.current.data = exp['current'] if 'current' in exp else False
    return render_template('user/edit-experience.html', exp=exp, e_form=form)

@user.route('message/send/<string:user_id>', methods=['POST'])
@login_required
def send_message(user_id):
    if request.method == 'POST':
        form = ChatForm()
        if form.validate_on_submit():
            data = {
                'receiver_id':user_id,
                'sender_id':session['user']['id'],
                'message':form.message.data,
                'status':'unread'
            }
            ChatService().create(data)
            flash('Message sent successfully.', 'success')
            return redirect(request.referrer)
        else:
            if form.errors:
                for error, msg in form.errors.items():
                    flash(msg[0], 'warning')
            return redirect(request.referrer)

@user.route('chats/<string:user_id>', methods=['GET'])
@login_required
def chats(user_id):
    # messages = ChatService().get_chats(user_id)
    # print(messages)
    messages = []
    return render_template('user/chats.html', messages=messages)