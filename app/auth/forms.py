from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp(
            r"^[a-zA-Z]+[a-zA-Z0-9._]*$", 0, 'Username must have only letters, figures, dotts or underscores')
    ])
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', 'Passwords must match')
    ])
    password2 = PasswordField('Confirm your password',
                              validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()
    ])
    submit = SubmitField('Reset password')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', 'Passwords must match')
    ])
    password2 = PasswordField(
        'Confirm your new password', validators=[DataRequired()])
    submit = SubmitField('Reset password')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', 'Passwords must match')
    ])
    password2 = PasswordField(
        'Confirm your new password', validators=[DataRequired()])
    submit = SubmitField('Change password')
