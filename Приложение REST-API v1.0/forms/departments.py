from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    chief = StringField('Руководитель', validators=[DataRequired()])
    members = StringField('Id участников', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
