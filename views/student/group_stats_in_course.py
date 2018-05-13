from flask import render_template, abort
from flask.views import View
from flask_login import current_user
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

    @staticmethod
    def group_of_user(user_id: int) ->Group:
        query = text("""SELECT *
                        FROM (user_groups
                        JOIN "group" ON user_groups.group_id = "group".group_id)
                        WHERE user_id = :user_id""")
        return [i for i in db.engine.execute(query, user_id=user_id)][0]

    @staticmethod
    def _users_in_group(group_id: int) -> list:
        query = text("""SELECT "user".id, "user".name
                        FROM user_groups JOIN "user" ON user_id = "user".id
                        WHERE group_id = :group_id""")
        return db.engine.execute(query, group_id=group_id)

    @staticmethod
    def _get_course(course_id) ->Course:
        return Course.query.get(course_id)

    @classmethod
    @cache.memoize(timeout=60*60)
    def generate_marks(cls, group: Group, course: int) -> list:
        students = ReportsProcessor._users_in_group(group.group_id)
        course = ReportsProcessor._get_course(course)
        marks_lst = []
        for i in students:
            reports = Report.query.filter_by(report_course=course.course_id,
                                             report_student=i.id).order_by(Report.report_num)
            marks_lst.append(cls(i, reports, course.labs_amount))
        return marks_lst

    @staticmethod
    def user_has_course(user: int, course: int) -> bool:
        query = text("""SELECT course.course_id
                        FROM
                        (SELECT course_id, user_id
                        FROM
                        group_courses
                        JOIN
                        user_groups ON group_courses.group_id = user_groups.group_id) as g
                        JOIN course ON g.course_id = course.course_id
                        WHERE user_id = :user_id--put some integer value""")
        result = [i.course_id for i in db.engine.execute(query, user_id=user)]
        return course in result


class GroupStats(View):
    def dispatch_request(self, *args, **kwargs):
        if not ReportsProcessor.user_has_course(current_user.id, kwargs.get('course')):
            abort(404)
        return render_template('group_stats.html',
                               marks=ReportsProcessor.generate_marks(ReportsProcessor.group_of_user(current_user.id),
                                                                     kwargs.get('course')))

