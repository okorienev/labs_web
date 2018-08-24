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
from flask_ckeditor import CKEditorField


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
    course = SelectField('course', choices=[], coerce=int, validators=[DataRequired()],
                         render_kw={'class': 'form-control'})


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
    report_group = SelectField(validators=[Optional()],
                               choices=[],
                               coerce=int,
                               render_kw={'placeholder': "Group", 'class': 'form-control'})


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
    course_name = StringField('course name',
                              validators=[DataRequired(),
                                          Length(min=10, max=50,
                                                 message="Course name should be between 10 and 50 characters")],
                              render_kw={'placeholder': 'Course Name',
                                         'class': 'form-control'})
    course_shortened = StringField('course shortened',
                                   validators=[DataRequired(),
                                               Length(min=1, max=5,
                                                      message="Short name should be between 1 and 5 characters")],
                                   render_kw={'placeholder': 'Course Shortened', 'class': 'form-control'})
    lab_max_score = IntegerField('max score', validators=[DataRequired(),
                                                          NumberRange(min=1, max=100,
                                                                      message="Max score should be between 1 & 100")],
                                 render_kw={'placeholder': 'Max score for each lab', 'class': 'form-control'})
    labs_amount = IntegerField('labs amount', validators=[DataRequired(),
                                                          NumberRange(min=1,
                                                                      max=15,
                                                                      message='Labs amount should be between 1 & 15')],
                               render_kw={'placeholder': 'Labs amount', 'class': 'form-control'})
    groups = SelectMultipleField('groups', coerce=int, choices=[], validators=[DataRequired()],
                                 render_kw={'placeholder': 'Groups', 'class': 'form-control form-control-lg'})
    attachment = FileField('course docs', validators=[
        FileRequired(),
        FileAllowed(['zip', 'rar', 'tar'], 'zip/rar/tar files only!')
    ],
                           render_kw={'class': 'form-control-file'})


class SearchArchiveForm(FlaskForm):
    report_group = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Group',
                                                                       'class': 'form-control'})
    report_student = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Student',
                                                                         'class': 'form-control'})
    report_number = IntegerField(validators=[DataRequired()], render_kw={'placeholder': 'Report number',
                                                                         'class': 'form-control'})
    report_course = SelectField(validators=[DataRequired()], coerce=int, render_kw={'placeholder': 'Course',
                                                                                    'class': 'form-control'})


class MakeAnnouncementForm(FlaskForm):
    title = StringField(validators=[DataRequired(message='Title cannot be empty'),
                                    Length(min=5, max=40, message="Title should be between 5 and 40 characters")],
                        render_kw={'placeholder': 'Announcement Title',
                                   'class': 'form-control'})
    body = CKEditorField(validators=[DataRequired(message='Body cannot be empty'),
                                     Length(max=10000, message='Body should be between less than 10000 characters')])
    groups = SelectMultipleField(choices=[],
                                 coerce=int,
                                 validators=[DataRequired(message='Choose at least one group to notify')],
                                 render_kw={'class': 'form-control'})
# TODO refactor all form fields to have error messages for each validator
