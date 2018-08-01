from flask.views import View
from flask_login import login_required, current_user
from flask import abort, render_template
from . import ReportsProcessor
from labs_web.extensions import Course, User, Report


def render_course_info(student: User, course: Course) -> str:
    """
    :param student:
    :param course: course to render
    :return: course info rendered into html (bootstrap 4) of given course with results of given student
    """
    results = ReportsProcessor(student,
                               course.labs_amount,
                               Report.query.filter_by(report_student=student.id))
    return render_template('student/course_representation.html',
                           course=course,
                           tutor=User.query.get(course.course_tutor),
                           results=results)


class StudentCourses(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        group = kwargs.get('group')
        if group is not current_user.group[0]:
            abort(404)
        return render_template('student/my_courses.html',
                               group=group,
                               reprs=[render_course_info(current_user, course) for course in group.courses])
