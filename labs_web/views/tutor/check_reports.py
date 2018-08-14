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
    works inside app context, makes all needed queries itself
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


class ReportRepr:
    """
    Class to query & store information about reports
    """
    def __init__(self, report: Report, course_shortened):
        """
        :param report: Report instance
        :param course_shortened: needed to generate download url without extra query
        """
        self.id = report.report_id
        self.uploaded = report.report_uploaded
        self.student = User.query.get(report.report_student)
        self.group = self.student.group[0].name
        self.number = report.report_num
        self.link = url_for('.get-report',
                            course=course_shortened,
                            group=self.group,
                            student=report.report_student,
                            number=report.report_num)

    @classmethod
    def from_list(cls, reports: list, course_shortened: str) -> list:
        """
        :param reports: list of reports
        :param course_shortened: shortened name of course
        :return: list of ReportRepr instances to insert into template
        !initializing each ReportRepr makes 2 queries (loading user & his group) 
        """
        return [cls(report, course_shortened) for report in reports]


class CheckReports(View):
    """View to check reports in course, commonly accessed via flask.redirect() from ChooseCourseToCheck view"""
    decorators = [login_required]
    methods = ["GET", "POST"]

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

    def dispatch_request(self, *args, **kwargs):
        form = CheckReportForm()
        search = ReportSearchingForm()
        course = Course.query.get(kwargs.get('course_id'))
        search.report_group.choices = [(i.group_id, i.name) for i in course.groups]
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
                return redirect(url_for('.tutor_check_reports', course_id=course.course_id))
            if search.validate_on_submit():
                searcher = ReportsSearcher(course)
                reports = ReportRepr.from_list(searcher.search(search.data.get('report_student'),
                                                               search.data.get('report_group'),
                                                               search.data.get('report_number')),
                                               course_shortened=course.course_shortened)
                return render_template('tutor/check_report.html', form=form, search=search,
                                       reports=reports)
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        default_pagination = Report.query.filter(Report.report_mark.is_(None),
                                                 Report.report_course == course.course_id).\
            paginate(page=page if page else 1, per_page=10)
        return render_template('tutor/check_report.html',
                               reports=ReportRepr.from_list(default_pagination.items, course.course_shortened),
                               current=default_pagination.page,
                               next=default_pagination.next_num,
                               prev=default_pagination.prev_num,
                               pages=default_pagination.pages,
                               form=form, search=search, course_id=course.course_id)
