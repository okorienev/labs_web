from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from views.tutor.choose_course_to_check import ChooseCourseToCheck
from views.tutor.check_reports import CheckReports
from views.tutor.download_report import DownloadReport
from views.tutor.courses_of_tutor_ajax import CoursesOfTutorXHR
from views.tutor.course_stats import CourseStats
from views.tutor.check_reports_menu_ajax import CheckReportsMenuAjax

tutor = Blueprint('tutor',
                  __name__,
                  url_prefix='/tutor')
tutor.add_url_rule('/choose-course/', view_func=ChooseCourseToCheck.as_view('tutor_choose_course'))
tutor.add_url_rule('/check/<int:course_id>/<int:page>/', view_func=CheckReports.as_view('tutor_check_reports'))
tutor.add_url_rule('/get-report/<course>/<group>/<student>/<int:number>/',
                   view_func=DownloadReport.as_view('get-report'))
tutor.add_url_rule('/stats/<int:course_id>', view_func=CourseStats.as_view('tutor_course_stats'))
tutor.add_url_rule('/courses_ajax/', view_func=CoursesOfTutorXHR.as_view('course_of_tutor'))
tutor.add_url_rule('/check-reports-menu-items/', view_func=CheckReportsMenuAjax.as_view('check_reports_menu'))


@tutor.before_request
@login_required
def i_am_tutor():
    if current_user.role != 2:  # should be changed to query in large app with many roles but not necessary in this case
        abort(403)


@tutor.route('/home/')
@login_required
def tutor_home():
    return render_template('tutor/tutor_home.html')


