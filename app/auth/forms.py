from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField, SearchField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.auth.service import UserService


def get_all_users():
    return UserService.get_all()

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = UserService.get_user_by_attr('email', email.data)
        if not user:
            raise ValidationError('Please check your credentials.')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('','Select Role'), ('Developer','Developer'), ('Hiring Manager','Hiring Manager')], validators=[
                                     DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if len(get_all_users()) != 0:
            user = UserService.get_user_by_attr('email', email.data)
            if user:
                raise ValidationError('That email is already registered.')

    def validate_username(self, username):
        if len(get_all_users()) != 0:
            user = UserService.get_user_by_attr('username', username.data)
            if user:
                raise ValidationError('That username is taken, Please choose a different one.')


class SearchForm(FlaskForm):
    category = SelectField(choices=[('', 'Select Category'), ('job', 'Jobs'), ('dev', 'Developers')], validators=[DataRequired()])
    q = SearchField(validators=[DataRequired()])