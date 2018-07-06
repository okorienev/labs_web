from flask import url_for, jsonify
from flask.views import View
from extensions.extensions import cache
from flask_login import login_required, current_user
from extensions.models import Course, Report


@cache.memoize(60*60)
def count_unchecked(course_id):
    return Report.query.filter_by(report_course=course_id,
                                  report_mark=None).count()


def drop_unchecked(*args, **kwargs):
    if kwargs.get('course_id'):
        cache.delete_memoized(count_unchecked, kwargs.get('course_id'))


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
