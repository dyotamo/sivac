from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField
from wtforms.validators import DataRequired
from forms.search import CHOICES


class LoginForm(FlaskForm):
    institution = SelectField('Institution', choices=CHOICES)
    password = PasswordField('Password', validators=[DataRequired()])
