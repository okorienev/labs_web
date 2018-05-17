from flask import flash, redirect, request, render_template, url_for
from flask.views import View
from extensions.extensions import db
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from extensions.forms import CourseChoosingForm


class ChooseCourse(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    @staticmethod
    def _courses_of_user(user_id: int) -> list:
        query = text("""SELECT course.course_id, course.course_shortened, course.course_name
                        FROM
                        (SELECT course_id, user_id
                        FROM
                        group_courses
                        JOIN
                        user_groups ON group_courses.group_id = user_groups.group_id) AS g
                        JOIN course ON g.course_id = course.course_id
                        WHERE user_id = :user_id""")
        return [i for i in db.engine.execute(query, user_id=user_id)]

    def dispatch_request(self):
        form = CourseChoosingForm()
        courses = ChooseCourse._courses_of_user(current_user.id)
        if request.method == "POST" and form.validate_on_submit():
            try:
                course_index = [i.course_shortened for i in courses].index(form.data.get('shortened'))
                return redirect(url_for('student.group_stats', course=courses[course_index].course_id))
            except ValueError:
                flash("course not present in list of available")
                return redirect(request.url)
        return render_template('student/choose_course.html', form=form, courses=courses)


