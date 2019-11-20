from flask_wtf import FlaskForm
from wtforms import SelectField, PasswordField
from wtforms.validators import DataRequired
from .search import CHOICES


class LoginForm(FlaskForm):
    institution = SelectField('Institution', choices=CHOICES)
    password = PasswordField('Password', validators=[DataRequired()])


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField(
        'Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])