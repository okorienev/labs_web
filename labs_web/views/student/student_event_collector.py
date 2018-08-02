from flask import jsonify
from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import Report, Course


def checked_reports(user_id: int, reports_amount: int) -> iter:
    checked = Report.query.filter(Report.report_student == user_id,
                                  Report.report_checked.isnot(None)).order_by(Report.report_checked.desc()). \
                                                                     limit(reports_amount)
    for report in checked:
        yield {'category': 'report-checked',
               'report_num': report.report_num,
               'course': Course.query.get(report.report_course).course_shortened,
               'mark': report.report_mark}


class StudentEventCollector(View):
    decorators = [login_required]

    def dispatch_request(self):
        events = [i for i in checked_reports(current_user.id, 10)]
        return jsonify(events)

