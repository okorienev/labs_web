from flask.views import View
from flask_login import login_required
from flask import abort


class GetCourseDocs(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        abort(418)
