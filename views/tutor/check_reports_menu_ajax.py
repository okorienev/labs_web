from flask import url_for, jsonify
from flask.views import View
from flask_login import login_required, current_user
from extensions.models import Course, Report


class CheckReportsMenuAjax(View):
    decorators = [login_required]

    def dispatch_request(self):
        return jsonify([
            {'shortened': course.course_shortened,
             'unchecked': Report.query.filter_by(report_course=course.course_id, report_mark=None).count(),
             'url': url_for('tutor.tutor_check_reports', course_id=course.course_id, page=1)
             }
            for course in Course.query.filter_by(course_tutor=current_user.id).all()
        ])
