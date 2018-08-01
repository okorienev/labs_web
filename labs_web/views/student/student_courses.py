from flask.views import View
from flask_login import login_required, current_user
from flask import render_template
from . import ReportsProcessor
from labs_web.extensions import Course, User, Report


class _Representation:
    """
    objects store data for template rendering
    """
    def __init__(self, student: User, course: Course):
        self.course = course
        self.results = ReportsProcessor(student,
                                        Report.query.filter_by(report_student=student.id,
                                                               report_course=course.course_id).all(),
                                        course.labs_amount)
        self.tutor = User.query.get(course.course_tutor)


class StudentCourses(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        group = current_user.group[0]
        return render_template('student/my_courses.html',
                               group=group,
                               reprs=[_Representation(current_user, course) for course in group.courses])
