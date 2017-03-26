from flask_wtf import Form
from wtforms import StringField, validators, Form, PasswordField
from wtforms.validators import DataRequired

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)], render_kw={"placeholder": "Username"})
    email = StringField('Email Address', [validators.Length(min=6, max=35)], render_kw={"placeholder": "Email"})
    password = PasswordField('New Password', [ validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={"placeholder": "Confirm Password"})


class LoginForm(Form):
    username = StringField('Username', render_kw={"placeholder": "Username"})
    password = PasswordField('Password', render_kw={"placeholder": "Password"})
