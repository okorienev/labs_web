from flask import Blueprint, abort, redirect, url_for
from flask_login import current_user
from views.student.group_stats_in_course import GroupStats
from views.student.student_send_report import SendReport

student = Blueprint('student',
                    __name__,
                    url_prefix='/student')
student.add_url_rule('/group-stats/<int:course>', view_func=GroupStats.as_view('group_stats'))
student.add_url_rule('/send-report/', view_func=SendReport.as_view('send_report'))


@student.before_request
def i_am_student():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.role != 1:  # should be changed to query in large app with many roles but not necessary in this case
        abort(403)
