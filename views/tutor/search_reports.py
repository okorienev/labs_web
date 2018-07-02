from extensions.models import Report, User, Group, Course


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
            group = Group.query.filter_by(name=group).first()
            if not group or group.group_id not in [group.group_id for i in self.course.groups]:
                return []
            if number_in_course:
                return self._search_by_group_and_number(group, number_in_course)
            else:
                return self._search_by_group(group)
        if number_in_course:
            return self._search_by_number(number_in_course)
        else:
            return []

    def _search_by_number(self, number: int):
        return Report.query.filter_by(report_course=self.course.course_id,
                                      report_num=number,
                                      report_mark=None).all()

    def _search_by_student_and_number(self, student: str, number):
        student_obj = User.query.filter(User.name.like('%'+student+'%')).first()
        if not student_obj:
            return []
        return Report.query.filter_by(report_course=self.course.course_id,
                                      report_num=number,
                                      report_student=student_obj.id,
                                      report_mark=None).all()

    def _search_by_student(self, student):
        student_obj = User.query.filter(User.name.like('%'+student+'%')).first()
        if not student_obj:
            return []
        return Report.query.filter_by(report_course=self.course.course_id,
                                      report_student=student_obj.id,
                                      report_mark=None).all()

    def _search_by_group(self, group: Group):
        reports = []
        for student in group.students:
            reports.extend(self._search_by_student(student.name))
        return reports

    def _search_by_group_and_number(self, group: Group, number: int):
        reports = []
        for student in group.students:
            print(student)
            print(self._search_by_student_and_number(student.name, number))
            reports.extend(self._search_by_student_and_number(student.name, number))
        return reports
