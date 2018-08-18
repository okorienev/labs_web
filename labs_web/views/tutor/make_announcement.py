from flask.views import MethodView
from flask_login import login_required
from flask import render_template


class MakeAnnouncement(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('tutor/make_announcement.html')

    def post(self):
        pass
