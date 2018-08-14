from labs_web.extensions import Report, User, Group, Course


class ReportsSearcher:
    def __init__(self, course: Course):
        self.course = course

    def search(self, student=None, group: int = None, number_in_course=None):
        if student:
            if number_in_course:
                return self._search_by_student_and_number(student, number_in_course)
            else:
                return self._search_by_student(student)
        if group:
            group_obj = Group.query.get(group)
            if number_in_course:
                return Report.query.filter(Report.report_student.in_(i.id for i in group_obj.students),
                                           Report.report_num == number_in_course,
                                           Report.report_course == self.course.course_id,
                                           Report.report_mark.is_(None)).all()
            else:
                return Report.query.filter(Report.report_student.in_(i.id for i in group_obj.students),
                                           Report.report_course == self.course.course_id,
                                           Report.report_mark.is_(None))
        if number_in_course:
            return Report.query.filter_by(report_course=self.course.course_id,
                                          report_num=number_in_course,
                                          report_mark=None).all()
        else:
            return []

    def _search_by_student_and_number(self, student: str, number):
        student_obj = User.query.filter(User.name.like('%' + student + '%')).first()
        if not student_obj:
            return []
        return Report.query.filter_by(report_course=self.course.course_id,
                                      report_num=number,
                                      report_student=student_obj.id,
                                      report_mark=None).all()

    def _search_by_student(self, student):
        student_obj = User.query.filter(User.name.like('%' + student + '%')).first()
        if not student_obj:
            return []
        return Report.query.filter_by(report_course=self.course.course_id,
                                      report_student=student_obj.id,
                                      report_mark=None).all()
