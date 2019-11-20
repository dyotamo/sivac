from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired

CHOICES = [("Universidade Zambeze", "Universidade Zambeze"),
           ("Universidade Eduardo Mondlane", "Universidade Eduardo Mondlane"),
           ("Universidade Pedagógica", "Universidade Pedagógica")]


class SearchForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    issue_date = DateField('Issue Date', format='%d/%m/%Y',
                           validators=[DataRequired()])
    institution = SelectField('Institution', choices=CHOICES)
