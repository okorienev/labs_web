from flask import request, render_template, abort, url_for, flash, redirect
from flask.views import View
from models import Course, User, db
from flask_login import login_required, current_user
from models import Report
from sqlalchemy.sql import text
from forms import CheckReportForm
from datetime import datetime, timezone


class CheckReports(View):
    """View to check reports in course, commonly accessed via flask.redirect() from ChooseCourseToCheck view"""
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self, *args, **kwargs):
        form = CheckReportForm()
        course_id = kwargs.get('course_id')
        course = Course.query.get(course_id)
        if course.course_tutor != current_user.id:
            abort(403)
        reports = [{'student': i.report_student,
                    'number': i.report_num,
                    'id': i.report_id,
                    'uploaded': i.report_uploaded,
                    'comment': i.report_stu_comment} for i in
                   Report.query.filter_by(
                       report_course=course_id,
                       report_mark=None).paginate(page=kwargs.get('page'),
                                                  error_out=True,
                                                  max_per_page=10).items]
        if request.method == "POST" and form.validate_on_submit():
            report_id = form.data.get('report_id')
            report_mark = form.data.get('report_mark')
            if not any([report_id == i.get('id') for i in reports]):  # report should be in  current Pagination
                flash("Report id is not present on this page, check your form")
                return redirect(request.url)
            if report_mark not in range(1, course.lab_max_score + 1):  # score should be correct
                flash("Wrong lab score, it should be in range from 1 up to {score}".format(score=course.lab_max_score))
                return redirect(request.url)
            report = Report.query.get(report_id)
            report.report_mark = report_mark
            report.report_checked = datetime.now(timezone.utc)
            report.report_tut_comment = form.data.get('tutor_comment')
            db.session.commit()
            return redirect(url_for('.tutor_check_reports', course_id=course_id, page=1))

        for i in reports:
            query = text("""SELECT *
                            FROM user_groups
                            JOIN "group" ON user_groups.group_id = "group".group_id
                            WHERE user_id = :user_id""")
            group = [j.name for j in db.engine.execute(query, user_id=i.get('student'))][0]
            i.update({'group': group,
                      'student': User.query.get(i.get('student')).name})
            i.update({'link': url_for('.get-report',
                                      course=course.course_shortened,
                                      group=group,
                                      student=i.get('student').split()[1],  # last name
                                      number=i.get('number'))})
        return render_template('check_report.html', reports=reports, form=form)

