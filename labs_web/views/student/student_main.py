from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required
from labs_web.extensions import report_sent
from labs_web.views.tutor.ajax.check_reports_menu_ajax import drop_unchecked
from . import (SendReport,
               ChooseCourse,
               GroupStats,
               ReportsProcessor,
               CoursesOfUserXHR,
               StudentCourses,
               GetCourseDocs,
               StudentEventCollector,
               MyReports,
               DownloadReport,
               Announcement,
               GetAnnouncementsAJAX)  # importing views


def report_sent_callback(*args, **kwargs):
    report_id = kwargs.get('report_id')
    if report_id:
        ReportsProcessor.drop_marks_cache.delay(report_id)
        drop_unchecked.delay(report_id)


student = Blueprint('student',
                    __name__,
                    url_prefix='/student')
student.add_url_rule('/group-stats/<int:course>', view_func=GroupStats.as_view('group_stats'))
student.add_url_rule('/send-report/', view_func=SendReport.as_view('send_report'))
student.add_url_rule('/choose-course/', view_func=ChooseCourse.as_view('choose_course'))
student.add_url_rule('/ajax/my-courses/', view_func=CoursesOfUserXHR.as_view('my_courses_xhr'))
student.add_url_rule('/my-courses/', view_func=StudentCourses.as_view('my_courses'))
student.add_url_rule('/course-docs/<int:course_id>', view_func=GetCourseDocs.as_view('course_docs'))
student.add_url_rule('/collect-events/', view_func=StudentEventCollector.as_view('collect_events'))
student.add_url_rule('/my-reports/', view_func=MyReports.as_view('my_reports'))
student.add_url_rule('/download-report/<int:report_id>/', view_func=DownloadReport.as_view('download-report'))
student.add_url_rule('/announcement/<announcement_id>/', view_func=Announcement.as_view('announcement'))
student.add_url_rule('/get-announcements-ajax/', view_func=GetAnnouncementsAJAX.as_view('get_announcements'))
report_sent.connect(report_sent_callback)


@student.before_request
@login_required
def i_am_student():
    if current_user.role != 1:  # should be changed to query in large app with many roles but not necessary in this case
        abort(403)


@student.route('/home/')
@login_required
def student_home():
    return render_template('student/student_home.html')
