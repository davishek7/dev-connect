from curses import flash
from email import message
from flask import render_template, request, flash, redirect, url_for
from . import contact
from .forms import ContactForm
from ..database import db, SCHEMA


@contact.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        data = request.form
        name = data['name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        db.insert(SCHEMA, 'contact', [{'name':name, 'email':email, 'subject':subject, 'message':message}])
        flash(f'Thank you {name} for contacting us. We will start working on your suggestions as soon as possible.')
        return redirect(url_for('auth.index'))
    return render_template('contact/contact.html', form=form)