from flask_wtf import FlaskForm
from wtforms import (PasswordField,
                     StringField,
                     BooleanField,
                     FileField,
                     TextAreaField,
                     IntegerField,
                     SelectField,
                     SelectMultipleField)
from wtforms.validators import DataRequired, Optional, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Username',
                                                                   'class': 'form-control'})
    password = PasswordField(validators=[DataRequired()], render_kw={'placeholder': 'Password',
                                                                     'class': 'form-control'})
    remember_me = BooleanField(default=False)


class ReportSendingForm(FlaskForm):
    number_in_course = IntegerField('', render_kw={'placeholder': 'Lab number',
                                                   'class': 'form-control'})
    course = SelectField(choices=[], validators=[DataRequired()], coerce=int, render_kw={'placeholder': 'Course',
                                                                                         'class': 'form-control'})
    attachment = FileField('report', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDF files only!')
    ],
                           render_kw={'class': 'form-control-file'})


class CourseChoosingForm(FlaskForm):
    shortened = StringField('course shortened name', validators=[DataRequired()],
                            render_kw={'placeholder': 'Course shortened',
                                       'class': 'form-control'})


class CheckReportForm(FlaskForm):
    report_id = IntegerField('report id', validators=[DataRequired()], render_kw={'placeholder': 'Report id',
                                                                                  'class': 'form-control'})
    report_mark = IntegerField('report mark', validators=[DataRequired()], render_kw={'placeholder': 'Report mark',
                                                                                      'class': 'form-control'})
    tutor_comment = TextAreaField('tutor comment', render_kw={'placeholder': 'Comment (optional)',
                                                              'class': 'form-control'})


class ReportSearchingForm(FlaskForm):
    report_student = StringField(validators=[Optional()], render_kw={'placeholder': 'Student',
                                                                     'class': 'form-control'})
    report_number = IntegerField(validators=[Optional()], render_kw={'placeholder': 'Report number',
                                                                     'class': 'form-control'})
    report_group = StringField(validators=[Optional()], render_kw={'placeholder': "Group",
                                                                   'class': 'form-control'})


class ForgotPasswordForm(FlaskForm):
    email = StringField('email', validators=[Email(), DataRequired()], render_kw={'placeholder': 'Email',
                                                                                  'class': 'form-control'})


class RestorePasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(),
                                                     Length(min=6, max=30,
                                                            message='minimal length is 6, maximal is 30')],
                             render_kw={'placeholder': 'New password',
                                        'class': 'form-control'})
    repeat = PasswordField('repeat', validators=[DataRequired(),
                                                 EqualTo('password', message='passwords should match')],
                           render_kw={'placeholder': 'Repeat password',
                                      'class': 'form-control'})


class AddCourseForm(FlaskForm):
    course_name = StringField('course name', validators=[DataRequired(), Length(max=50)],
                              render_kw={'placeholder': 'Course Name', 'class': 'form-control'})
    course_shortened = StringField('course shortened', validators=[DataRequired(), Length(max=5)],
                                   render_kw={'placeholder': 'Course Shortened', 'class': 'form-control'})
    lab_max_score = IntegerField('max score', validators=[DataRequired(), NumberRange(min=1, max=100)],
                                 render_kw={'placeholder': 'Max score in lab', 'class': 'form-control'})
    labs_amount = IntegerField('labs amount', validators=[DataRequired(),
                                                          NumberRange(min=1,
                                                                      max=15,
                                                                      message='should be between 1 and 15')],
                               render_kw={'placeholder': 'Labs amount', 'class': 'form-control'})
    groups = SelectMultipleField('groups', choices=[], validators=[DataRequired()],
                                 render_kw={'placeholder': 'Groups', 'class': 'form-control form-control-lg'})
