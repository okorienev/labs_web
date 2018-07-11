from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from . import (ChooseCourseToCheck,
               CheckReports,
               DownloadReport,
               CoursesOfTutorXHR,
               CourseStats,
               CheckReportsMenuAjax)
from labs_web.extensions import report_checked
from labs_web.views.student.group_stats_in_course import ReportsProcessor
from .check_reports_menu_ajax import drop_unchecked


def report_checked_callback(*args, **kwargs):
    report_id = kwargs.get('report_id')
    if report_id:
        ReportsProcessor.drop_marks_cache.delay(report_id)
        drop_unchecked.delay(report_id)


tutor = Blueprint('tutor',
                  __name__,
                  url_prefix='/tutor')
tutor.add_url_rule('/choose-course/', view_func=ChooseCourseToCheck.as_view('tutor_choose_course'))
tutor.add_url_rule('/check/<int:course_id>', view_func=CheckReports.as_view('tutor_check_reports'))
tutor.add_url_rule('/get-report/<course>/<group>/<student>/<int:number>/',
                   view_func=DownloadReport.as_view('get-report'))
tutor.add_url_rule('/stats/<int:course_id>', view_func=CourseStats.as_view('tutor_course_stats'))
tutor.add_url_rule('/courses_ajax/', view_func=CoursesOfTutorXHR.as_view('course_of_tutor'))
tutor.add_url_rule('/check-reports-menu-items/', view_func=CheckReportsMenuAjax.as_view('check_reports_menu'))
report_checked.connect(report_checked_callback)


@tutor.before_request
@login_required
def i_am_tutor():
    if current_user.role != 2:  # should be changed to query in large app with many roles but not necessary in this case
        abort(403)


@tutor.route('/home/')
@login_required
def tutor_home():
    return render_template('tutor/tutor_home.html')


