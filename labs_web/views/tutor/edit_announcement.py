from flask.views import View
from flask_login import current_user, login_required
from labs_web.extensions import (get_announcement_by_oid,
                                 Announcements,
                                 MakeAnnouncementForm,
                                 mongo_oid,
                                 announcement_made)
from flask import render_template, flash, redirect, url_for, request, abort, g, jsonify
from .make_announcement import group_form_choices
from bson.objectid import ObjectId, InvalidId
import datetime
from functools import wraps


def _may_interact_with_announcement(f):
    """decorator to check tutor permissions for given announcements"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        announcement = get_announcement_by_oid(kwargs.get("announcement_id"))
        if not announcement or announcement['tutor']['id'] != current_user.id:
            abort(404)
        g.announcement = announcement
        return f(*args, **kwargs)
    return wrapper


class TutorAnnouncement(View):
    decorators = [login_required, _may_interact_with_announcement]
    methods = ["GET", "POST", "DELETE"]

    def dispatch_request(self, *args, **kwargs):
        announcement = g.announcement
        if request.method == "DELETE":
            announcement_made.send(id=kwargs.get('announcement_id'))
            Announcements.delete_one({'_id': mongo_oid(kwargs.get('announcement_id'))})
            return jsonify({
                'text': 'announcement {} successfully deleted'.format(announcement['_id'])
            })
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
                announcement_made.send(id=kwargs.get('announcement_id'))
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
