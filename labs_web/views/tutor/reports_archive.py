from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import Course, Report, SearchArchiveForm, User, Group
from flask import render_template, abort, request, flash, redirect
from sqlalchemy import and_
from .check_reports import ReportRepr


class ArchiveRepr(ReportRepr):
    """
    adds three fields to parent class: mark, course and check date 
    """

    def __init__(self, report: Report, course_shortened):
        self.mark = report.report_mark
        self.course = course_shortened
        self.checked = report.report_checked
        super().__init__(report, course_shortened)

    @classmethod
    def from_list(cls, reports: list, course_shortened: str):
        return [cls(report, course_shortened) for report in reports]


class ReportsArchive(View):
    methods = ["GET", "POST"]
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        form = SearchArchiveForm()
        form.report_course.choices = [(i.course_id, "{} - {}".format(i.course_name, i.course_shortened)) for i in
                                      Course.query.filter(Course.course_tutor == current_user.id).all()]
        if request.method == "POST" and form.validate_on_submit():
            course = Course.query.get(form.data.get('report_course'))
            group = Group.query.filter(Group.name == form.data.get('report_group')).first()
            if not group or course.course_id not in [course.course_id for course in group.courses]:
                flash('Group doesnt exist or doesnt have the selected course')
                return redirect(request.url)
            student = User.query.filter(and_(User.name.like('%' + form.data.get('report_student') + '%'),
                                             User.id.in_([i.id for i in group.students]))).first()
            if not student:
                flash('Student doesnt exist or doesnt belong to the selected group')
                return redirect(request.url)
            reports = Report.query.filter(
                Report.report_course == course.course_id,
                Report.report_student == student.id,
                Report.report_mark.isnot(None),
                Report.report_num == form.data.get('report_number')).all()
            if not reports:
                flash('No reports corresponding given criteria found')
            return render_template('tutor/reports_archive.html', form=form, reports=ArchiveRepr.from_list(
                reports, course_shortened=course.course_shortened))
        return render_template('tutor/reports_archive.html', form=form)
