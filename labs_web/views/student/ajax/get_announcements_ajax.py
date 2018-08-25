from flask.views import View
from flask import jsonify, url_for
from flask_login import login_required, current_user
from labs_web.extensions import Announcements, cache, celery


@cache.memoize(60 * 60 * 24)
def announcements_of_group(group_id: int) -> list:
    return [i for i in Announcements.find({'groups': {"$in": [group_id]}},
                                          {"_id": 1, "title": 1, "tutor": 1, "date": 1}).sort("date", -1)]


@celery.task(ignore_result=True)
def drop_announcements_of_group(group_id: int) -> None:
    cache.delete_memoized(announcements_of_group, group_id)


class GetAnnouncementsAJAX(View):
    decorators = [login_required]

    def dispatch_request(self):
        return jsonify([{'title': i['title'],
                         'link': url_for('student.announcement', announcement_id=str(i['_id'])),
                         'tutor': i['tutor']['name'],
                         'date': i['date']} for i in announcements_of_group(current_user.group[0].group_id)])
