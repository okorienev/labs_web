from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import CourseSnapshotForm, redis_conn
from flask import render_template,request, flash
from datetime import timedelta


class CourseSnapshot(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        timeout = redis_conn.pttl('snapshot-timeout-{}'.format(current_user.id))
        form = CourseSnapshotForm()
        form.course.choices = [(course.course_id, course.course_name) for course in current_user.courses]
        if request.method == "POST" and form.validate_on_submit():
            pass
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)
        return render_template('tutor/course_snapshot.html',
                               form=form,
                               timeout=timedelta(timeout))
