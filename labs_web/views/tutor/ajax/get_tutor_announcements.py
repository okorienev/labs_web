from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import Announcements, cache, celery
from flask import url_for, jsonify


@cache.memoize(60 * 60 * 24)
def tutor_announcements(tutor_id: int):
    return [i for i in Announcements.find({'tutor.id': tutor_id},
                                          {'title': 1, '_id': 1, 'date': 1}).sort("date", -1)]


@celery.task(ignore_result=True)
def drop_tutor_announcements(tutor_id: int):
    cache.delete_memoized(tutor_announcements, tutor_id)


class GetTutorAnnouncements(View):
    decorators = [login_required]

    def dispatch_request(self):
        return jsonify([{
            'title': item['title'],
            'link': url_for('tutor.announcement', announcement_id=str(item['_id'])),
            'date': item['date']
        } for item in tutor_announcements(current_user.id)])
