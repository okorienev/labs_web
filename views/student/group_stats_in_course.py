from flask import render_template, abort
from flask.views import View
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from extensions.extensions import cache
from extensions.models import User, Course, Group, Report, db


class ReportsProcessor:
    def __init__(self, student: User, reports, max_reports: int):
        self.name = student.name
        self.reports = ['N/A' for i in range(max_reports)]
        self.sum = sum([i.report_mark for i in reports if i.report_mark])
        for i in reports:
            self.reports[i.report_num - 1] = i.report_mark if i.report_mark else 'N/C'

    def __repr__(self):
        return "Reports list of {name}:".format(name=self.name) + " ".join([str(i) for i in self.reports])

    @classmethod
    @cache.memoize(timeout=60*60)
    def generate_marks(cls, group: Group, course: int) -> list:
        course = Course.query.get(course)
        students = [i for i in group.students]
        marks_lst = []
        for i in students:
            reports = Report.query.filter_by(report_course=course.course_id,
                                             report_student=i.id).order_by(Report.report_num)
            marks_lst.append(cls(i, reports, course.labs_amount))
        return marks_lst

    @staticmethod
    def user_has_course(user: int, course: int) -> bool:
        group = User.query.get(user).group[0]
        courses_of_stu = [i.course_id for i in group.courses]
        return course in courses_of_stu


class GroupStats(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        if not ReportsProcessor.user_has_course(current_user.id, kwargs.get('course')):
            abort(404)
        return render_template('student/group_stats.html',
                               marks=ReportsProcessor.generate_marks(current_user.group[0],
                                                                     kwargs.get('course')))

