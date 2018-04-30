from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SelectField, FileField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField(default=False)


class ReportSendingForm(FlaskForm):
    number_in_course = IntegerField('')
    course = StringField('course shortened name', validators=[DataRequired()])
    comment = TextAreaField()
    attachment = FileField('report', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])


class CourseChoosingForm(FlaskForm):
    shortened = StringField('course shortened name', validators=[DataRequired()])


class CheckReportForm(FlaskForm):
    report_id = IntegerField('report id', validators=[DataRequired()])
    report_mark = IntegerField('report mark', validators=[DataRequired()])
    tutor_comment = TextAreaField('tutor comment')


