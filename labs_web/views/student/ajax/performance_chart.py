from flask.views import View
from flask_login import login_required, current_user
from labs_web.extensions import User, db, Report, cache, Course
from flask import jsonify, abort
from random import randint, choice
import datetime


def performance_of_lab(lab_number: int, user_id: int, course_id: int):
    user = User.query.get(user_id)
    marks_of_group = [report.report_mark for report in Report.query.filter(Report.report_num == lab_number,
                                                                           Report.report_student.in_(
                                                                               [i.id for i in user.group[0].students]),
                                                                           Report.report_course == course_id,
                                                                           Report.report_mark.isnot(None)).all()]

    marks_of_course = [report.report_mark for report in Report.query.filter(Report.report_num == lab_number,
                                                                            Report.report_course == course_id,
                                                                            Report.report_mark.isnot(None)).all()]

    lab_of_student = Report.query.filter(Report.report_num == lab_number,
                                         Report.report_student == user_id,
                                         Report.report_course == course_id,
                                         Report.report_mark.isnot(None)).first()
    return [lab_number,
            lab_of_student.report_mark if lab_of_student else 0,
            round((sum(marks_of_group) / len(marks_of_group) if len(marks_of_group) != 0 else 0), 2),
            round((sum(marks_of_course) / len(marks_of_course) if len(marks_of_course) != 0 else 0), 2)]


class PerformanceChartAjax(View):
    decorators = [login_required]

    def dispatch_request(self, *args, **kwargs):
        # for course in current_user.group[0].courses:  # fill db with random test data
        #     for group in course.groups:
        #         for i in range(20):
        #             student = choice(group.students)
        #             lab_num = randint(1, course.labs_amount)
        #             report = Report(report_student=student.id,
        #                             report_mark=randint(3, course.lab_max_score),
        #                             report_num=randint(1, course.labs_amount),
        #                             report_uploaded=datetime.datetime.utcnow(),
        #                             report_course=course.course_id,
        #                             report_hash="fake")
        #             db.session.add(report)
        # db.session.commit()
        course = Course.query.get(kwargs.get('course_id'))
        if course.course_id not in [i.course_id for i in current_user.group[0].courses]:
            abort(403)
        return jsonify(
            {'name': course.course_name,
             'labs': course.labs_amount,
             'shortened': course.course_shortened,
             'data': ([performance_of_lab(i, current_user.id, course.course_id)
                       for i in range(1, course.labs_amount + 1)])
             })
