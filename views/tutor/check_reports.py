from datetime import datetime, timezone
from flask import request, render_template, abort, url_for, flash, redirect
from flask.views import View
from flask_login import login_required, current_user
from extensions.extensions import cache
from extensions.forms import CheckReportForm, ReportSearchingForm
from extensions.models import Course, User, db
from extensions.models import Report


class CheckReports(View):
    """View to check reports in course, commonly accessed via flask.redirect() from ChooseCourseToCheck view"""
    decorators = [login_required]
    methods = ["GET", "POST"]

    @staticmethod
    def generate_reports(course_id: int) -> list:
        return [{'student': i.report_student,
                 'number': i.report_num,
                 'id': i.report_id,
                 'uploaded': i.report_uploaded,
                 'comment': i.report_stu_comment} for i in
                Report.query.filter_by(report_course=course_id,
                                       report_mark=None).limit(10)]

    @staticmethod
    def _set_report_mark(report_id: int, mark: int, comment="") -> None:
        report = Report.query.get(report_id)
        report.report_mark = mark
        report.report_checked = datetime.now(timezone.utc)
        report.report_tut_comment = comment
        db.session.commit()

    @staticmethod
    def report_can_not_be_checked(report_id: int, tutor_id: int, report_mark: int):
        """
        :param report_id: 
        :param tutor_id: 
        :return: true if given report can be checked by the given tutor
        :return: list with errors to flash 
        """
        tutor = User.query.get(tutor_id)
        report = Report.query.get(report_id)
        if not report:
            return "Report doesn't exist"
        course = Course.query.get(report.report_course)
        if course.course_tutor != tutor.id:
            return "You don't have permission to check this report"
        if report.report_mark:
            return "Report is already checked"
        if report_mark not in range(1, course.lab_max_score + 1):
            return "Report mark should be between 1 and {} inclusive".format(course.lab_max_score)

    @staticmethod
    def generate_reports_representation(reports: list, course_shortened: str) -> list:
        for report in reports:
            group = User.query.get(report.get('student')).group[0]
            report.update({'group': group.name,
                           'student': User.query.get(report.get('student')).name})
            report.update({'link': url_for('.get-report',
                                           course=course_shortened,
                                           group=group.name,
                                           student=report.get('student').split()[1],  # last name
                                           number=report.get('number'))})
        return reports

    def dispatch_request(self, *args, **kwargs):
        form = CheckReportForm()
        search = ReportSearchingForm()
        course = Course.query.get(kwargs.get('course_id'))
        reports = CheckReports.generate_reports(course.course_id)
        if request.method == "POST" and form.validate_on_submit():
            report_id = form.data.get('report_id')
            report_mark = form.data.get('report_mark')
            error = CheckReports.report_can_not_be_checked(report_id, current_user.id, report_mark)
            if error:
                flash(error)
                return redirect(request.url)
            CheckReports._set_report_mark(report_id, report_mark, form.data.get("tutor_comment"))
            return redirect(url_for('.tutor_check_reports', course_id=course.course_id))
        reports = CheckReports.generate_reports_representation(reports, course.course_shortened)
        return render_template('tutor/check_report.html', reports=reports, form=form, search=search)
