from flask.views import View
from flask import jsonify, url_for
from flask_login import login_required, current_user
from labs_web.extensions import Announcements


class GetAnnouncementsAJAX(View):
    decorators = [login_required]

    def dispatch_request(self):
        result = [i for i in Announcements.find({'groups': {"$in": [current_user.group[0].group_id]}},
                                                {"_id": 1, "title": 1, "tutor": 1, "date": 1})]
        return jsonify([{'title': i['title'],
                         'link': url_for('student.announcement', announcement_id=str(i['_id'])),
                         'tutor': i['tutor'],
                         'date': i['date']} for i in result])
