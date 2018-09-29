# Deprecated AJAX handler
from flask import url_for, jsonify
from flask.views import View
from flask_login import current_user, login_required


class CoursesOfUserXHR(View):
    decorators = [login_required]

    def dispatch_request(self):
        courses = [{'url': url_for('student.group_stats', course=i.course_id),
                   'name': i.course_shortened}
                   for i in current_user.group[0].courses]   # relation is many-to-many to avoid nullable foreign keys
        return jsonify(courses)                              # so user.group returns list instead of a single item
