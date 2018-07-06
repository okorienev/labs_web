from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required
from views.student.group_stats_in_course import GroupStats, ReportsProcessor
from views.student.student_send_report import SendReport
from views.student.choose_course import ChooseCourse
from views.student.courses_of_user_ajax import CoursesOfUserXHR
from extensions.signals import report_sent
from views.tutor.check_reports_menu_ajax import drop_unchecked

student = Blueprint('student',
                    __name__,
                    url_prefix='/student')
student.add_url_rule('/group-stats/<int:course>', view_func=GroupStats.as_view('group_stats'))
student.add_url_rule('/send-report/', view_func=SendReport.as_view('send_report'))
student.add_url_rule('/choose-course/', view_func=ChooseCourse.as_view('choose_course'))
student.add_url_rule('/ajax/my-courses/', view_func=CoursesOfUserXHR.as_view('my_courses_xhr'))
report_sent.connect(ReportsProcessor.drop_marks_cache)
report_sent.connect(drop_unchecked)


@student.before_request
@login_required
def i_am_student():
    if current_user.role != 1:  # should be changed to query in large app with many roles but not necessary in this case
        abort(403)


@student.route('/home/')
@login_required
def student_home():
    return render_template('student/student_home.html')
