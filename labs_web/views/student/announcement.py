from flask.views import View
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, flash
from labs_web.extensions import get_announcement_by_oid


class Announcement(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        announcement = get_announcement_by_oid(kwargs.get('announcement_id'))
        if not announcement:
            flash('Announcement not found')
            return redirect(url_for('student.student_home'))
        if current_user.group[0].group_id not in announcement.get('groups'):
            flash("You have no rights to view this announcement")
            return redirect(url_for('student.student_home'))
        return render_template('student/announcement.html',
                               announcement=announcement)

