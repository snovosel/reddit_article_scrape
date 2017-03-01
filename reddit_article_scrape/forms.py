from flask_wtf import Form
from wtforms import StringField, BooleanField, validators, Form, PasswordField
from wtforms.validators import DataRequired

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [ validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')
