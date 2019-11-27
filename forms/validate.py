from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired

CHOICES = [("Universidade Zambeze", "Universidade Zambeze"),
           ("Universidade Eduardo Mondlane", "Universidade Eduardo Mondlane"),
           ("Universidade Pedagógica", "Universidade Pedagógica")]


class ValidateForm(FlaskForm):
    code = StringField("Código", validators=[
                       DataRequired(message="Este campo é obrigatório.")])
    issue_date = DateField("Data de Emissão", format="%d/%m/%Y",
                           validators=[DataRequired(message="Formato inválido. Use dd/mm/aaaa")])
    institution = SelectField("Instituição", choices=CHOICES)
