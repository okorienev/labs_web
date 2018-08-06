from flask.views import View
from flask_login import login_required
from flask import render_template
from labs_web.extensions import AddCourseForm, Group


class AddCourse(View):
    decorators = [login_required]

    def dispatch_request(self):
        form = AddCourseForm()
        form.groups.choices = [(group.group_id, group.name) for group in Group.query.all()]
        return render_template('tutor/add_course.html',
                               form=form)
