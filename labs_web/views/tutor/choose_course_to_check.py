# Deprecated view
from flask import render_template, request, redirect, url_for
from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import CourseChoosingForm


class ChooseCourseToCheck(View):
    """View to choose course to check reports in"""
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = CourseChoosingForm()
        form.course.choices = [(course.course_id, course.course_name) for course in current_user.courses]
        if request.method == "POST" and form.validate_on_submit():
            return redirect(url_for('.tutor_check_reports', course_id=form.data.get('course'), page=1))
        return render_template('tutor/tutor_choose_course.html', courses=current_user.courses, form=form)







