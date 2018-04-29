from flask import request, render_template, abort
from flask.views import View
from models import Course, User
from flask_login import login_required, current_user
from models import Report


class CheckReports(View):
    decorators = [login_required]
    """View to check reports in course, commonly accessed via flask.redirect() from ChooseCourseToCheck view"""
    def dispatch_request(self, *args, **kwargs):
        course = Course.query.get(request.args.get('course_id'))
        if course.course_tutor != current_user.id:
            abort(403)
        course_id = request.args.get('course_id')
        reports = [{'student': i.report_student,
                    'number': i.report_num,
                    'id': i.report_id,
                    'uploaded': i.report_uploaded,
                    'comment': i.report_stu_comment} for i in
                   Report.query.filter_by(report_course=course_id, report_mark=None).limit(20).all()]
        for i in reports:
            i.update({'student': User.query.get(i.get('student')).name})
        return render_template('check_report.html', reports=reports)

