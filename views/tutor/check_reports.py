from flask.views import View
from flask_login import login_required, current_user
from models import Report


class CheckReports(View):
    decorators = [login_required]
    """View to check reports in course, commonly accessed via flask.redirect() from ChooseCourseToCheck view"""
    def dispatch_request(self, *args, **kwargs):
        course_id = kwargs.get('course_id')
        reports = [{'student' :i.report_student,
                    'number': i.report_num,
                    'id': i.report_id,
                    'comment': i.report_stu_comment} for i in
                   Report.query.filter_by(report_course=course_id, report_mark=None).limit(20).all()]
        
