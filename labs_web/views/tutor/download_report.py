from os.path import join

from flask import send_file, abort, flash, redirect, url_for, current_app
from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import Course, Report


class DownloadReport(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        if Course.query.filter_by(course_shortened=kwargs.get('course')).first().course_tutor != current_user.id:
            abort(404)  # aborts when trying to check not own course
        try:
            return send_file(join(current_app.config.get('UPLOAD_PATH'),
                                  kwargs.get('course'),
                                  kwargs.get('group'),
                                  str(kwargs.get('student')),
                                  (str(kwargs.get('number')) + '.pdf')))
        except FileNotFoundError:
            flash('Report file was not found, please contact the website administration')
            return redirect(url_for('tutor.tutor_check_reports'))
