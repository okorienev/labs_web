from flask import url_for, jsonify
from flask.views import View
from flask_login import current_user, login_required
from views.student.choose_course import ChooseCourse


class CoursesOfUserXHR(View):
    decorators = [login_required]

    def dispatch_request(self):
        courses = [{'url': url_for('student.group_stats', course=i.course_id),
                   'name': i.course_shortened}
                   for i in ChooseCourse.courses_of_user(current_user.id)]
        return jsonify(courses)
