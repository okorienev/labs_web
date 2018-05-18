from flask.views import View
from flask import redirect, render_template, abort
from flask_login import login_required, current_user
from extensions.models import Course
from sqlalchemy.sql import text
from extensions.extensions import db
from views.student.group_stats_in_course import ReportsProcessor as rp


class CourseStats(View):
    methods = ["GET"]
    decorators = [login_required]

    @staticmethod
    def _groups_in_course(course_id: int) ->list:
        query = text("""SELECT "group".group_id, "group".name
                        FROM "group"
                        JOIN group_courses ON group_courses.group_id = "group".group_id
                        WHERE course_id = :course_id""")
        return [i for i in db.engine.execute(query, course_id=course_id)]

    @staticmethod
    def _generate_group_tables(groups: list, course: int):
        return [{'group': i.name,
                 'marks': rp.generate_marks(i, course)} for i in groups]

    def dispatch_request(self, *args, **kwargs):
        if not Course.query.get(kwargs.get('course_id')).course_tutor == current_user.id:
            abort(404)
        return render_template('tutor/course_stats.html',
                               group_reports=CourseStats._generate_group_tables(
                                   CourseStats._groups_in_course(kwargs.get('course_id')),
                                   course=kwargs.get('course_id')))


