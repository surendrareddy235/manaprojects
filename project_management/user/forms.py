from flask_wtf import FlaskForm
from wtforms.validators import  DataRequired,Email,EqualTo
from wtforms import  StringField,PasswordField,SubmitField
class LoginForm(FlaskForm):
    user_mail = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    user_mail = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')