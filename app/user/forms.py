from email.policy import default
from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectMultipleField, SubmitField, TextAreaField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from app.auth.forms import get_all_users
from app.auth.service import UserService


SKILL_CHOICES = {
    'Backend':['flask', 'expressjs', 'django', 'Laravel', 'Spring Boot', 'FastAPI', 'Nextjs', 'Nestjs', 'Nuxtjs'],
    'Frontend':['Reactjs', 'Vuejs', 'Angular', 'Svelte'],
    'Mobile':['Android', 'iOS', 'React Native', 'Flutter', 'Ionic'],
    'Language':['Python', 'Java', 'Javascript', 'Ruby', 'PHP', 'Typescript', 'C', 'C++', 'Go', 'Rust', 'Dart', 'Swift', 'Kotlin'],
    'Database':['PostgreSQL', 'MySQL', 'MongoDB', 'HarperDB', 'SQLite'],
    'Cloud Tech':['Amazon Web Services', 'Google Cloud Platform', 'Digital Ocean', 'Microsoft Azure', 'Linode', 'Netlify', 'Vercel', 'Railway', 'Heroku 🥲']
}

STATUS_CHOICES = [('', 'Select Status'), ('Open to work', 'Open to Work'), ('Busy', 'Busy')]


class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    skills = SelectMultipleField('Skills', choices=SKILL_CHOICES, validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    status = SelectField('Select Work Status', choices=STATUS_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_email(self, email):
        if len(get_all_users()) != 0:
            user = UserService.get_user_by_attr('email', email.data)
            if user and session['user']['id'] != user[0]['id']:
                raise ValidationError('That email is already registered.')

    def validate_username(self, username):
        if len(get_all_users()) != 0:
            user = UserService.get_user_by_attr('username', username.data)
            if user and session['user']['id'] != user[0]['id']:
                raise ValidationError('That username is taken, Please choose a different one.')


class ExperienceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    start_date = DateField(format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField(format='%Y-%m-%d')
    current = BooleanField('I currently work here', default=False)

    submit = SubmitField('Save')

    def validate_end_date(self, end_date):
        if end_date.data:
            if self.start_date.data > end_date.data:
                raise ValidationError("Start date can't be greater than end date")


class ChatForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])