from flask.views import View
from flask_login import login_required, current_user
from flask import render_template, request, flash
from labs_web.extensions import Course, MakeAnnouncementForm, Announcements
import datetime


class MakeAnnouncement(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        # forming set of unique options
        form = MakeAnnouncementForm()
        form.groups.choices = set().union(*[{(group.group_id, group.name) for group in course.groups}
                                            for course in
                                            Course.query.filter(Course.course_tutor == current_user.id).all()])
        if request.method == "POST" and form.validate_on_submit():
            Announcements.insert_one({
                'tutor': {
                    'name': current_user.name,
                    'id': current_user.id
                },
                'title': form.data.get('title'),
                'body': form.data.get('body'),
                'groups': form.data.get('groups'),
                'date': datetime.datetime.utcnow()
            })
            flash('Announcement successfully made')
        for field, message in form.errors:
            flash(message)
        return render_template('tutor/make_announcement.html', form=form)
