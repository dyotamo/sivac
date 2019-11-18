from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    issue_date = DateField('Issue Date', format='%d/%m/%Y', validators=[DataRequired()])
    institution = SelectField('Institution', choices=[
                              ("UZ", "UZ"), ("UEM", "UEM"), ("UP", "UP")])
