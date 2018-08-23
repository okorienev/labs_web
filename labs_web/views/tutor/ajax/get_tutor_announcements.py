from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import Announcements
from flask import url_for, jsonify


class GetTutorAnnouncements(View):
    decorators = [login_required]

    def dispatch_request(self):
        announcements = Announcements.find({'tutor.id': current_user.id},
                                           {'title': 1, '_id': 1, 'date': 1})
        return jsonify([{
            'title': item['title'],
            'link': url_for('tutor.announcement', announcement_id=str(item['_id'])),
            'date': item['date']
        } for item in announcements])
