from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    user_type = SelectField('Who are you?',
                            choices=[('student', 'Student'), ('tutor', 'Tutor')], validators=[DataRequired()])
    remember_me = BooleanField(default=False)
