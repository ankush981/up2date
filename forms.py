from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField, validators

class LoginForm(Form):
    email = TextField("Email address", validators=[validators.required(), validators.Email(message="That's not an email address!")])
    password = PasswordField("Password", validators=[validators.required()])
    remember_me = BooleanField("Remember me next time", default=True)
    submit = SubmitField("Login")

class RegForm(Form):
    email = TextField("Email address", validators=[validators.required(), validators.Email(message="That's not an email address!")])
    password = PasswordField("Password", validators=[validators.required()])
    submit = SubmitField("Register!")