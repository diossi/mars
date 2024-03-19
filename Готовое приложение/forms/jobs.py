from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = StringField('Id капитана', validators=[DataRequired()])
    job = StringField('Вид работы', validators=[DataRequired()])
    collaborators = StringField('Id участников', validators=[DataRequired()])
    work_size = StringField('Время работы(в часах)', validators=[DataRequired()])
    is_finished = BooleanField('Закончена?')
    submit = SubmitField('Подтвердить')
