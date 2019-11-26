from flask_wtf import FlaskForm
from wtforms import SelectField, PasswordField
from wtforms.validators import DataRequired

from .validate import CHOICES


class LoginForm(FlaskForm):
    institution = SelectField('Instituição', choices=CHOICES)
    password = PasswordField('Password', validators=[DataRequired()])


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField(
        'Password corrente', validators=[DataRequired()])
    new_password = PasswordField('Password nova', validators=[DataRequired()])
    confirm_new_password = PasswordField(
        'Password nova', validators=[DataRequired()])
