from flask import jsonify
from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import Report, Course, cache, User, celery
from typing import Iterator
from labs_web import app


@cache.memoize(60 * 60 * 12)
def checked_reports(user_id: int, reports_amount: int = 5) -> Iterator:
    checked = Report.query.filter(Report.report_student == user_id,
                                  Report.report_checked.isnot(None)).order_by(Report.report_checked.desc()). \
        limit(reports_amount)
    return [{'category': 'report-checked',
             'report_num': report.report_num,
             'course': Course.query.get(report.report_course).course_shortened,
             'mark': report.report_mark} for report in checked]


@celery.task(ignore_result=True)
def drop_checked_reports_cache(report_id: int):
    with app.app_context():
        cache.delete_memoized(checked_reports, User.query.get(Report.query.get(report_id).report_student).id)


class StudentEventCollector(View):
    decorators = [login_required]

    def dispatch_request(self):
        events = [i for i in checked_reports(current_user.id)]
        return jsonify(events)
