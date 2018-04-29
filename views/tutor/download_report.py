from flask import send_file, abort
from flask.views import View
from flask_login import login_required, current_user
from models import Course
from config import Config
from os.path import join


class DownloadReport(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        if Course.query.filter_by(course_shortened=kwargs.get('course')).first().course_tutor != current_user.id:
            abort(403)
        return send_file(join(Config.UPLOAD_PATH,
                              kwargs.get('course'),
                              kwargs.get('group'),
                              kwargs.get('student'),
                              (str(kwargs.get('number')) + '.pdf')))
