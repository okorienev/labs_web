from flask.views import View
from flask_login import current_user, login_required
from .course_snapshot import snapshot_is_mine
from flask import abort, send_file, current_app
import os.path as p


class DownloadSnapshot(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        name = kwargs.get('snapshot_name')
        print(name)
        if snapshot_is_mine(name):
            return send_file(p.join(current_app.config['UPLOAD_PATH'], 'snapshots', name),
                             attachment_filename=name,
                             as_attachment=True)
        abort(404)
