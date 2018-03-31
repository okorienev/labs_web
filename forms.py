from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SelectField, FileField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    user_type = SelectField('Who are you?',
                            choices=[('student', 'Student'), ('tutor', 'Tutor')], validators=[DataRequired()])
    remember_me = BooleanField(default=False)


class ReportSendingForm(FlaskForm):
    def __init__(self, courses):
        self.courses = courses
        super(ReportSendingForm, self).__init__()

    course = SelectField('Select course', choices=self.courses)
    number_in_course = IntegerField('')
    attachment = FileField('report', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    comment = TextAreaField()

