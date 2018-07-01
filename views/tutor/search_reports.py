from flask.views import View
from extensions.forms import ReportSearchingForm
from extensions.models import Report, User, Group, Course
from flask import jsonify
from flask_login import current_user, login_required


class ReportsSearcher:
    def __init__(self, course: Course):
        self.course = course

    def search(self, student=None, group=None, number_in_course=None):
        if student:
            if number_in_course:
                return self._search_by_student_and_number(student, number_in_course)
            else:
                return self._search_by_student(student)
        if group:
            if number_in_course:
                pass
            else:
                pass
        if number_in_course:
            return self._search_by_number(number_in_course)
        else:
            return None

    def _search_by_number(self, number: int):
        return Report.query.filter_by(report_course=self.course.course_id,
                                      report_num=number).all()

    def _search_by_student_and_number(self, student: str, number):
        student_id = User.query.filter_by(name=student).first().id
        return Report.query.filter_by(report_course=self.course.course_id,
                                      report_num=number,
                                      report_student=student_id).all()

    def _search_by_student(self, student):
        student_id = User.query.filter_by(name=student).first().id
        return Report.query.filter_by(report_course=self.course.course_id,
                                      report_student=student_id).all()

    def _search_by_group(self, group_name: str):
        group = Group.query.filter_by(name=group_name)
        if group.group_id not in [group.group_id for i in self.course.groups]:
            return None



class SearchReports(View):
    decorators = [login_required]
    methods = ["POST"]

    def dispatch_request(self, *args, **kwargs):
        form = ReportSearchingForm()
        if form.validate_on_submit():
            course = Course.query.get(kwargs.get('course_id'))
            if not course or course.course_tutor != current_user.id:
                return jsonify({'error': 'You don\'t have permission to query reports of this course'})
            searcher = ReportsSearcher(course)
            reports = searcher.search(form.data.get('report_student'),
                                      form.data.get('report_group'),
                                      form.data.get('report_number'))


