from flask import request, render_template, abort, url_for
from flask.views import View
from models import Course, User, db
from flask_login import login_required, current_user
from models import Report
from sqlalchemy.sql import text


class CheckReports(View):
    decorators = [login_required]
    """View to check reports in course, commonly accessed via flask.redirect() from ChooseCourseToCheck view"""
    def dispatch_request(self, *args, **kwargs):
        course = Course.query.get(kwargs.get('course_id'))
        if course.course_tutor != current_user.id:
            abort(403)
        course_id = kwargs.get('course_id')

        reports = [{'student': i.report_student,
                    'number': i.report_num,
                    'id': i.report_id,
                    'uploaded': i.report_uploaded,
                    'comment': i.report_stu_comment} for i in
                   Report.query.filter_by(report_course=course_id, report_mark=None).limit(20).all()]

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
        return render_template('check_report.html', reports=reports)

