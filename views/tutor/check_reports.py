from datetime import datetime, timezone
from flask import request, render_template, abort, url_for, flash, redirect
from flask.views import View
from flask_login import login_required, current_user
from extensions.extensions import cache
from extensions.forms import CheckReportForm
from extensions.models import Course, User, db
from extensions.models import Report


class CheckReports(View):
    """View to check reports in course, commonly accessed via flask.redirect() from ChooseCourseToCheck view"""
    decorators = [login_required]
    methods = ["GET", "POST"]

    @staticmethod
    @cache.memoize(timeout=60*60)
    def _generate_reports(course_id: int, page: int) -> list:
        return [{'student': i.report_student,
                 'number': i.report_num,
                 'id': i.report_id,
                 'uploaded': i.report_uploaded,
                 'comment': i.report_stu_comment} for i in
                Report.query.filter_by(report_course=course_id,
                                       report_mark=None).paginate(page=page,
                                                                  error_out=True,
                                                                  max_per_page=10).items]

    @staticmethod
    def _set_report_mark(report_id: int, mark: int, comment="") -> None:
        report = Report.query.get(report_id)
        report.report_mark = mark
        report.report_checked = datetime.now(timezone.utc)
        report.report_tut_comment = comment
        db.session.commit()

    @staticmethod
    def _generate_reports_representation(reports: list, course_shortened: str) -> list:
        for report in reports:
            group = User.query.get(report.get('student')).group[0]
            report.update({'group': group,
                           'student': User.query.get(report.get('student')).name})
            report.update({'link': url_for('.get-report',
                                           course=course_shortened,
                                           group=group,
                                           student=report.get('student').split()[1],  # last name
                                           number=report.get('number'))})
        return reports

    def dispatch_request(self, *args, **kwargs):
        form = CheckReportForm()
        course = Course.query.get(kwargs.get('course_id'))
        if course.course_tutor != current_user.id:
            abort(403)
        reports = CheckReports._generate_reports(course.course_id, kwargs.get('page'))
        if request.method == "POST" and form.validate_on_submit():
            report_id = form.data.get('report_id')
            report_mark = form.data.get('report_mark')
            if not any([report_id == i.get('id') for i in reports]):  # report should be in  current Pagination
                flash("Report id is not present on this page, check your form")
                return redirect(request.url)
            if report_mark not in range(1, course.lab_max_score + 1):  # score should be correct
                flash("Wrong lab score, it should be in range from 1 up to {score}".format(score=course.lab_max_score))
                return redirect(request.url)
            return redirect(url_for('.tutor_check_reports', course_id=course.course_id, page=1))
        reports = CheckReports._generate_reports_representation(reports, course.course_shortened)
        return render_template('tutor/check_report.html', reports=reports, form=form)
