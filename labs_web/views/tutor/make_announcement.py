from flask.views import View
from flask_login import login_required, current_user
from flask import render_template, jsonify, request
from collections import namedtuple
from labs_web.extensions import Course, MakeAnnouncementForm


class MakeAnnouncement(View):
    decorators = [login_required]

    def dispatch_request(self):
        # forming set of unique options
        form = MakeAnnouncementForm()
        form.groups.choices = set().union(*[{(group.group_id, group.name) for group in course.groups}
                                            for course in
                                            Course.query.filter(Course.course_tutor == current_user.id).all()])
        return render_template('tutor/make_announcement.html', form=form)
