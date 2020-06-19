from flask.views import View
from flask_login import current_user, login_required

from labs_web.extensions import minio
from labs_web.extensions.models import File
from flask import abort, send_file


class DownloadSnapshot(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        file = File.query.get(kwargs.get('file_id')) or abort(404)
        if file.file_type != File.Type.snapshot:
            abort(404)
        if file.owner_id != current_user.id:
            abort(403)

        file_obj = minio.client.get_object(file.bucket, file.key)
        return send_file(file_obj, attachment_filename=file.file_name, as_attachment=True)
