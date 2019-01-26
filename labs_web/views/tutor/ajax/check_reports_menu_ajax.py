# Deprecated AJAX handler
from flask import url_for, jsonify
from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import Course, Report, cache, celery
from labs_web import app


@cache.memoize(60*60)
def count_unchecked(course_id):
    return Report.query.filter_by(report_course=course_id,
                                  report_mark=None).count()


@celery.task(ignore_result=True)
def drop_unchecked(report_id: int):
    with app.app_context():
        report = Report.query.get(report_id)
        cache.delete_memoized(count_unchecked, report.report_course)


class CheckReportsMenuAjax(View):
    decorators = [login_required]

    def dispatch_request(self):
        return jsonify([
            {'shortened': course.course_shortened,
             'unchecked': count_unchecked(course.course_id),
             'url': url_for('tutor.tutor_check_reports', course_id=course.course_id)
             }
            for course in Course.query.filter_by(course_tutor=current_user.id).all()
        ])
