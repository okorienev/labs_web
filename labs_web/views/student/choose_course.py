from flask import flash, redirect, request, render_template, url_for
from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import CourseChoosingForm, User


class ChooseCourse(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = CourseChoosingForm()
        courses = [i for i in User.query.get(current_user.id).group[0].courses]
        if request.method == "POST" and form.validate_on_submit():
            try:
                course_index = [i.course_shortened for i in courses].index(form.data.get('shortened'))
                return redirect(url_for('student.group_stats', course=courses[course_index].course_id))
            except ValueError:
                flash("course not present in list of available")
                return redirect(request.url)
        return render_template('student/choose_course.html', form=form, courses=courses)


