from flask.views import View
from flask_login import current_user, login_required
from flask import render_template, url_for
from labs_web.extensions import Report, Course


class MyReports(View):
    decorators = [login_required]

    def dispatch_request(self):
        reports = sorted(current_user.reports, key=lambda report: report.report_uploaded, reverse=True)
        course_dict = {course.course_id: course.course_shortened for course in
                       current_user.group[0].courses}
        for report in reports:
            report.report_course = course_dict.get(report.report_course)
        return render_template('student/my_reports.html',
                               checked=[i for i in filter(lambda report: report.report_mark is not None, reports)],
                               unchecked=[i for i in filter(lambda report: report.report_mark is None, reports)])
