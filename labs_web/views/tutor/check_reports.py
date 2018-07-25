from datetime import datetime, timezone
from flask import request, render_template, abort, url_for, flash, redirect
from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import (celery,
                                 mail,
                                 report_checked,
                                 CheckReportForm,
                                 ReportSearchingForm,
                                 Course,
                                 User,
                                 db,
                                 Report)
from .search_reports import ReportsSearcher
from labs_web import app
from flask_mail import Message


@celery.task(ignore_result=True)
def send_mail_report_checked(report_id):
    """
    background task to notify students when their reports were checked by the tutor
    """
    with app.app_context():
        report = Report.query.get(report_id)
        student = User.query.get(report.report_student)
        course = Course.query.get(report.report_course)
        msg = Message()
        msg.sender = 'labs.web.notifications'
        msg.recipients = [student.email]
        msg.subject = "Report checked"
        msg.html = render_template('mail/report-checked.html',
                                   report=report,
                                   student=student,
                                   course=course)
        mail.send(msg)


class CheckReports(View):
    """View to check reports in course, commonly accessed via flask.redirect() from ChooseCourseToCheck view"""
    decorators = [login_required]
    methods = ["GET", "POST"]

    @staticmethod
    def generate_reports_default(course_id: int) -> list:
        return [{'student': i.report_student,
                 'number': i.report_num,
                 'id': i.report_id,
                 'uploaded': i.report_uploaded,
                 'comment': i.report_stu_comment} for i in
                Report.query.filter_by(report_course=course_id,
                                       report_mark=None).limit(10)]

    @staticmethod
    def generate_reports(reports: list):
        return [{'student': i.report_student,
                 'number': i.report_num,
                 'id': i.report_id,
                 'uploaded': i.report_uploaded,
                 'comment': i.report_stu_comment} for i in reports]

    @staticmethod
    def _set_report_mark(report: Report, mark: int, comment="") -> None:
        """
        set mark for given report and commits result to db
        all validations are done before with report_can_not_be_checked  
        :param report: Report object 
        :param mark: report mark
        :param comment: tutor comment
        :return: 
        """
        report.report_mark = mark
        report.report_checked = datetime.now(timezone.utc)
        report.report_tut_comment = comment
        db.session.commit()

    @staticmethod
    def report_can_not_be_checked(report: Report, course: Course, report_mark: int):
        """
        :param course: Course object 
        :param report: Report object
        :param report_mark: mark to put
        :return: None if given report can be checked by the given tutor
        :return: Error string if any error occurred during validating form data
        """
        if not report:
            return "Report doesn't exist"
        if report.report_mark:
            return "Report is already checked"
        if report_mark not in range(1, course.lab_max_score + 1):
            return "Report mark should be between 1 and {} inclusive".format(course.lab_max_score)

    @staticmethod
    def generate_reports_representation(reports: list, course_shortened: str) -> list:
        for report in reports:
            group = User.query.get(report.get('student')).group[0]
            report.update({'group': group.name,
                           'student': User.query.get(report.get('student'))})
            report.update({'link': url_for('.get-report',
                                           course=course_shortened,
                                           group=group.name,
                                           student=str(report.get('student').id),
                                           number=report.get('number'))})
        return reports

    def dispatch_request(self, *args, **kwargs):
        form = CheckReportForm()
        search = ReportSearchingForm()
        course = Course.query.get(kwargs.get('course_id'))
        if not course or course.course_tutor != current_user.id:
            abort(404)
        if request.method == "POST":
            if form.validate_on_submit():
                report = Report.query.get(form.data.get('report_id'))
                report_mark = form.data.get('report_mark')
                error = CheckReports.report_can_not_be_checked(report, course, report_mark)
                if error:
                    flash(error)
                    return redirect(request.url)
                CheckReports._set_report_mark(report, report_mark, form.data.get("tutor_comment"))
                report_checked.send(report_id=report.report_id)
                send_mail_report_checked.delay(report.report_id)
                return redirect(url_for('.tutor_check_reports', course_id=course.course_id))
            if search.validate_on_submit():
                searcher = ReportsSearcher(course)
                reports = CheckReports.generate_reports(searcher.search(search.data.get('report_student'),
                                                        search.data.get('report_group'),
                                                        search.data.get('report_number')))
                return render_template('tutor/check_report.html', form=form, search=search,
                                       reports=CheckReports.generate_reports_representation(reports,
                                                                                            course.course_shortened))
        reports = CheckReports.generate_reports_default(course.course_id)
        reports = CheckReports.generate_reports_representation(reports, course.course_shortened)
        return render_template('tutor/check_report.html', reports=reports, form=form, search=search)
