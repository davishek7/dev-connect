from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired
from app.user.forms import SKILL_CHOICES


TYPE_CHOICES = ['Remote', 'On-site', 'Hybrid']
EMPLOYMENT_TYPE = ['Full-time', 'Part-time', 'Internship']

class JobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    skills = SelectMultipleField('Skills', choices=SKILL_CHOICES, validators=[DataRequired()])
    job_type = SelectField('Workplace Type', choices=TYPE_CHOICES, validators=[DataRequired()])
    emp_type = SelectField('Employment Type', choices=EMPLOYMENT_TYPE, validators=[DataRequired()])
    submit = SubmitField('Save')