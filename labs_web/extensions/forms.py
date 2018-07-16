from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, FileField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional, Email
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField(validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    remember_me = BooleanField(default=False)


class ReportSendingForm(FlaskForm):
    number_in_course = IntegerField('', render_kw={'placeholder': 'Lab number'})
    course = StringField('course shortened name', validators=[DataRequired()], render_kw={'placeholder': 'Course'})
    # comment = TextAreaField(render_kw={'placeholder': 'Comment(optional)'})
    attachment = FileField('report', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])


class CourseChoosingForm(FlaskForm):
    shortened = StringField('course shortened name', validators=[DataRequired()],
                            render_kw={'placeholder': 'Course shortened'})


class CheckReportForm(FlaskForm):
    report_id = IntegerField('report id', validators=[DataRequired()], render_kw={'placeholder': 'Report id'})
    report_mark = IntegerField('report mark', validators=[DataRequired()], render_kw={'placeholder': 'Report mark'})
    tutor_comment = TextAreaField('tutor comment', render_kw={'placeholder': 'Comment (optional)'})


class ReportSearchingForm(FlaskForm):
    report_student = StringField(validators=[Optional()], render_kw={'placeholder': 'Student'})
    report_number = IntegerField(validators=[Optional()], render_kw={'placeholder': 'Report number'})
    report_group = StringField(validators=[Optional()], render_kw={'placeholder': "Group"})


class ForgotPasswordForm(FlaskForm):
    email = StringField('email', validators=[Email(), DataRequired()], render_kw={'placeholder': 'Email'})
