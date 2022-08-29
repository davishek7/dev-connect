from flask import render_template, redirect, url_for, flash, session, request
from . import jobs
from .forms import JobForm
from .service import JobService
from app.auth.service import UserService
from .decorators import job_owner_required
from app.auth.decorators import hiring_manager_required, developer_required, login_required
from datetime import datetime


@jobs.route('/list', methods=['GET'])
@jobs.route('/list/<string:user_id>', methods=['GET'])
def job_list(user_id=None):
    jobs = JobService.get_all()
    for job in jobs:
        job['__createdtime__'] = datetime.strptime(
            job['__createdtime__'], '%d-%m-%Y %I:%M %p').strftime('%B %d, %Y')
    return render_template('jobs/list.html', jobs=jobs)


@jobs.route('/create', methods=['GET', 'POST'])
@login_required
@hiring_manager_required
def create():
    form = JobForm()
    if form.validate_on_submit():
        job = {
            'title': form.title.data,
            'company': form.company.data,
            'location': form.location.data,
            'skills': form.skills.data,
            'job_type': form.job_type.data,
            'emp_type': form.emp_type.data,
            'description': form.description.data,
            'owner': session['user']['id'],
            'applicants': []
        }
        JobService().create(job)
        flash('New job created successfully', 'success')
        return redirect(url_for('user.profile', username=session['user']['username']))
    return render_template('jobs/job.html', form=form)


@jobs.route('/update/<string:id>', methods=['GET', 'POST'])
@login_required
@hiring_manager_required
@job_owner_required
def update(id):
    form = JobForm()
    job = JobService().get_job(id)
    if form.validate_on_submit():
        job = {
            'title': form.title.data,
            'company': form.company.data,
            'location': form.location.data,
            'skills': form.skills.data,
            'job_type': form.job_type.data,
            'emp_type': form.emp_type.data,
            'description': form.description.data,
        }
        JobService().update(id, job)
        flash('Job updated successfully', 'success')
        return redirect(url_for('user.profile', username=session['user']['username']))
    if request.method == 'GET':
        form.title.data = job['title']
        form.company.data = job['company']
        form.location.data = job['location']
        form.skills.data = job['skills']
        form.job_type.data = job['job_type']
        form.emp_type.data = job['emp_type']
        form.description.data = job['description']
    return render_template('jobs/job.html', form=form, job=job)


@jobs.route('/details/<string:id>', methods=['GET', 'POST'])
@login_required
def details(id):
    job = JobService().get_job(id)
    job['__createdtime__'] = datetime.strptime(
            job['__createdtime__'], '%d-%m-%Y %I:%M %p').strftime('%B %d, %Y')
    user = UserService().get_user(job['owner'])[0]
    return render_template('jobs/details.html', job=job, user=user)


@jobs.route('/bookmark/<string:id>', methods=['GET'])
@login_required
@developer_required
def bookmark(id):
    bookmarks = UserService().bookmark(session['user']['id'], id)
    session['user']['bookmarks'] = bookmarks[0]
    if bookmarks[1] == 'add':
        flash('Job bookmarked successfully', 'success')
    else:
        flash('Job removed from bookmark', 'info')
    return redirect(request.referrer)


@jobs.route('/apply/<string:id>', methods=['GET', 'POST'])
@login_required
@developer_required
def apply(id):
    JobService().apply(id, session['user']['id'])
    return redirect(request.referrer)
