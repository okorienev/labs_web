from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import get_announcement_by_oid, Announcements, MakeAnnouncementForm
from flask import render_template, flash, redirect, url_for, request
from .make_announcement import group_form_choices
from bson.objectid import ObjectId, InvalidId
import datetime


class TutorAnnouncement(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self, *args, **kwargs):
        announcement = get_announcement_by_oid(kwargs.get("announcement_id"))
        if not announcement or announcement['tutor']['id'] != current_user.id:
            flash('You don\'t have rights to view this announcement')
            return redirect(url_for('tutor.tutor_home'))
        form = MakeAnnouncementForm(title=announcement['title'],
                                    body=announcement['body'],
                                    groups=announcement['groups'])
        form.groups.choices = group_form_choices()
        if request.method == "POST" and form.validate_on_submit():
            try:
                oid = ObjectId(kwargs.get("announcement_id"))
                Announcements.find_one_and_update({'_id': oid},
                                                  {"$set": {'body': form.data.get('body'),
                                                            'groups': form.data.get('groups'),
                                                            'edited': datetime.datetime.utcnow(),
                                                            'title': form.data.get('title')}
                                                   })
                flash("Announcement successfully updated")
                return redirect(url_for("tutor.tutor_home"))
            except InvalidId:
                flash("Announcement id is invalid")
                return redirect(url_for('tutor.tutor_home'))
            except TypeError:
                flash("Announcement id is invalid")
                return redirect(url_for('tutor.tutor_home'))
        for field, message in form.errors:
            flash(message)
        return render_template('tutor/make_announcement.html',
                               form=form)
