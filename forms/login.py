from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    institution = SelectField('Institution', choices=[(
        "Universidade Zambeze", "Universidade Zambeze")])
    password = PasswordField('Password', validators=[DataRequired()])
