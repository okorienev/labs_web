from datetime import datetime, timezone
from hashlib import md5
from flask import render_template, redirect, request, flash
from flask.views import View
from flask_login import current_user, login_required
from labs_web.config import Config
from labs_web.extensions import (ReportSendingForm,
                                 report_sent,
                                 User,
                                 Report,
                                 db,
                                 Course)
import os.path as p
import os


def courses_of_user(user_id: int) -> list:
    """:returns course list of given user"""
    return [{'name': i.course_name, 'shortened': i.course_shortened}
            for i in User.query.get(user_id).group[0].courses]


def add_report_to_database(course_id: int, student_id: int, report_num, hash_md5: str):
    # creating new report
    report = Report(
        report_course=course_id,
        report_student=student_id,
        report_num=report_num,
        report_stu_comment="",
        report_uploaded=datetime.now(timezone.utc),
        report_hash=hash_md5
    )
    # adding report to database
    db.session.add(report)
    db.session.commit()
    flash('Report successfully sent')


def create_user_folder_structure(course: Course, student: User) -> None:
    """
    creates proper folder structure when first report is uploaded by the student
    structure should be <course_shortened>/<group_name>/<student_id>/<lab_number>.pdf
    :return: None
    """
    course_folder = p.join(Config.UPLOAD_PATH, course.course_shortened)
    if not p.exists(course_folder) or not p.isdir(course_folder):
        os.mkdir(course_folder)
    group_folder = p.join(course_folder, student.group[0].name)
    if not p.exists(group_folder) or not p.isdir(group_folder):
        os.mkdir(group_folder)
    student_folder = p.join(group_folder, str(student.id))
    if not p.exists(student_folder) or not p.isdir(student_folder):
        os.mkdir(student_folder)


class SendReport(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = ReportSendingForm()
        user_courses = courses_of_user(current_user.id)

        if request.method == 'POST' and form.validate_on_submit():
            course = Course.query.filter_by(course_shortened=form.data.get('course')).first()
            group = current_user.group[0]
            report_number = form.data.get('number_in_course')
            if not course or course.course_id not in [course.course_id for course in group.courses]:
                flash('You don\'t have this course')
                return redirect(request.url)
            report = Report.query.filter_by(report_course=course.course_id,
                                            report_student=current_user.id,
                                            report_num=report_number).first()
            if report and report.report_mark:
                flash('This work was already checked')
                return redirect(request.url)
            if report_number not in range(1, int(course.labs_amount) + 1):
                flash('lab number out of range')  # lab number should be in range between 1 and max lab number in course
                return redirect(request.url)
            # file uploading
            file = form.attachment.data
            if (lambda filename: '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf')(file.filename):
                filename = str(report_number) + '.pdf'  # filename is <number_in_course>.pdf
                # saving file to uploads
                filepath = p.join(Config.UPLOAD_PATH,
                                  course.course_shortened,
                                  group.name,
                                  str(current_user.id),
                                  filename)
                try:
                    file.save(filepath)
                except FileNotFoundError:
                    create_user_folder_structure(course, current_user)
                    file.save(filepath)
                # generating md5 for report
                hash_md5 = md5()
                try:
                    with open(filepath, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b''):  # read file by small chunks
                            hash_md5.update(chunk)
                except FileNotFoundError:
                    flash('some error occurred while saving your file, please retry')
                    return redirect(request.url)

                if not report:
                    add_report_to_database(course.course_id, current_user.id, report_number,
                                           hash_md5.hexdigest())
                else:
                    report.report_hash = hash_md5.hexdigest()
                    report.report_uploaded = datetime.now()
                    db.session.commit()
                    flash('Report was successfully updated')
                report = Report.query.filter_by(report_course=course.course_id,
                                                report_num=report_number,
                                                report_student=current_user.id).first()
                report_sent.send(report_id=report.report_id)
        return render_template('student/send_report.html',
                               user=current_user,
                               form=form,
                               courses=user_courses)
