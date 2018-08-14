from flask.views import View
from flask_login import login_required, current_user
from flask import send_file, abort, current_app, flash, url_for, redirect
import os.path as p
from labs_web.extensions import Report, Course


class DownloadReport(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        report = Report.query.get(kwargs.get('report_id'))
        if report and report.report_student == current_user.id:
            try:
                return send_file(p.join(current_app.config.get('UPLOAD_PATH'),
                                        Course.query.get(report.report_course).course_shortened,
                                        current_user.group[0].name,
                                        str(current_user.id),
                                        str(report.report_num) + '.pdf'))
            except FileNotFoundError:
                flash('Report was not found, please contact service administration')
                return redirect(url_for('student.student_home'))
        abort(404)
