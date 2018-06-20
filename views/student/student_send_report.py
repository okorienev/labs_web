from datetime import datetime, timezone
from hashlib import md5
from os.path import join
from flask import render_template, redirect, request, flash
from flask.views import View
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from config import Config
from extensions.forms import ReportSendingForm
from extensions.models import *


def courses_of_user(user_id: int) -> list:
    """:returns course list of given user"""
    return [{'name': i.course_name, 'shortened': i.course_shortened}
            for i in User.query.get(user_id).group[0].courses]


def group_of_user(user_id: int) -> Group:
    """:returns group of given user"""
    return User.query.get(user_id).group[0]


def lab_max_number(course: str) -> int:
    """:returns maximal number of work in requested course"""
    return Course.query.filter_by(course_shortened=course).one().labs_amount


def report_is_checked(course, number_in_course, user):
    """:returns report check status"""
    course = Course.query.filter_by(course_shortened=course).first()
    report = Report.query.filter_by(report_student=user,
                                    report_course=course.course_id,
                                    report_num=number_in_course).first()
    return report and report.report_mark


class SendReport(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = ReportSendingForm()
        user_courses = courses_of_user(current_user.id)

        if request.method == 'POST' and form.validate_on_submit():
            list_of_shortened = [i['shortened'] for i in user_courses]
            if request.form.get('course') not in list_of_shortened:  # user's group should have this course
                flash('You don\'t have this course')
                return redirect(request.url)
            # report for lab shouldn't be already checked
            if report_is_checked(form.data.get('course'), form.data.get('number_in_course'), current_user.id):
                flash('This work was already checked')
                return redirect(request.url)

            lab_max_amount = lab_max_number(request.form.get('course'))
            if form.data.get('number_in_course') not in range(1, int(lab_max_amount)):
                flash('lab number out of range')  # lab number should be in range between 1 and max lab number in course
                return redirect(request.url)
            # file uploading
            file = form.attachment.data
            if (lambda filename: '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf')(file.filename):
                filename = request.form.get('number_in_course') + '.pdf'  # filename is <number_in_course>.pdf

                group = group_of_user(current_user.id)
                # saving file to uploads
                file.save(join(Config.UPLOAD_PATH,
                               request.form.get('course'),
                               group.name,
                               current_user.name.split()[1],
                               filename))
                # generating md5 for report
                hash_md5 = md5()
                with open(join(Config.UPLOAD_PATH,
                               request.form.get('course'),
                               group.name,
                               current_user.name.split()[1],
                               filename), 'rb') as f:
                    for chunk in iter(lambda: f.read(4096),
                                      b''):  # read file by small chunks to avoid problems with memory
                        hash_md5.update(chunk)
                # creating new report
                report = Report(
                    report_course=Course.query.filter_by(course_shortened=request.form.get('course')).first().course_id,
                    report_student=current_user.id,
                    report_num=request.form.get('number_in_course'),
                    report_stu_comment=request.form.get('comment'),
                    report_uploaded=datetime.now(timezone.utc),
                    report_hash=hash_md5.hexdigest()
                )
                # adding report to database
                db.session.add(report)
                db.session.commit()
                flash('Report successfully sent')
        return render_template('student/send_report.html',
                               user=current_user,
                               form=form,
                               courses=user_courses)
