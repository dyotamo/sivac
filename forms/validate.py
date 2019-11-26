from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired

CHOICES = [("Universidade Zambeze", "Universidade Zambeze"),
           ("Universidade Eduardo Mondlane", "Universidade Eduardo Mondlane"),
           ("Universidade Pedagógica", "Universidade Pedagógica")]


class ValidateForm(FlaskForm):
    code = StringField("Código", validators=[DataRequired()])
    issue_date = DateField("Data de Emissão", format="%d/%m/%Y",
                           validators=[DataRequired()])
    institution = SelectField("Instituição", choices=CHOICES)
