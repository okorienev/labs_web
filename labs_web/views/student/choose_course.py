from flask import redirect, request, render_template, url_for
from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import CourseChoosingForm


class ChooseCourse(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = CourseChoosingForm()
        form.course.choices = [(course.course_id,
                                course.course_name) for course in current_user.group[0].courses]
        if request.method == "POST" and form.validate_on_submit():
                return redirect(url_for('student.group_stats', course=form.data.get('course')))
        return render_template('student/choose_course.html', form=form, courses=current_user.group[0].courses)


