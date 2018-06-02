from flask.views import View
from flask import jsonify, url_for
from extensions.models import Course
from flask_login import login_required, current_user


class CoursesOfTutorHXR(View):
    decorators = [login_required]

    def dispatch_request(self):
        # courses = [i for i in Course.query.filter_by(course_tutor=current_user.id).all()]
        return jsonify([
            {'name': i.course_shortened,
             'url': url_for('tutor.tutor_course_stats', course_id=i.course_id)}
            for i in [j for j in Course.query.filter_by(course_tutor=current_user.id).all()]
        ])
