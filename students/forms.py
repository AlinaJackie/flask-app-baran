
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField ,PasswordField, StringField
from wtforms.validators import DataRequired, Email
from wtforms.validators import DataRequired, EqualTo
from .models import Group

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    group = SelectField('Group', coerce=int)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])