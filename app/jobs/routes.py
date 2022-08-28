from flask import render_template, redirect, url_for, flash, session
from . import jobs
from .forms import JobForm
from .service import JobService
from .decorators import job_owner_required
from app.auth.decorators import hiring_manager_required, developer_required, login_required


@jobs.route('/create', methods=['GET','POST'])
@login_required
@hiring_manager_required
def create():
    form = JobForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        owner = session['user']['id']
        JobService().create_job([{'title':title, 'description':description, 'owner':owner}])
        flash('New job created successfully', 'success')
        return redirect(url_for('user.profile'))
    return render_template('jobs/create.html', form=form)

@jobs.route('/update/<string:id>', methods=['GET','POST'])
@login_required
@hiring_manager_required
@job_owner_required
def update(id):
    form = JobForm()
    job = JobService().get_job(id)
    return render_template('jobs/update.html', form=form, job=job)

@jobs.route('/delete/<string:id>', methods=['POST'])
@login_required
@hiring_manager_required
@job_owner_required
def delete(id):
    form = JobForm()
    job = JobService().get_job(id)

@jobs.route('/bookmark/<string:id>', methods=['POST'])
@login_required
@developer_required
def bookmark(id):
    job = JobService().get_job(id)
    return redirect(url_for('user.profile'))

# @jobs.route('/')