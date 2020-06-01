from labs_web.extensions import db
from hashlib import sha256

# table to link users to their roles, unused
roles = db.Table('user_roles',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('role_id', db.Integer, db.ForeignKey('role.role_id')))

# table to link users to their groups
groups = db.Table('user_groups',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('group_id', db.Integer, db.ForeignKey('group.group_id')))

# table to link groups with their courses
courses = db.Table('group_courses',
                   db.Column('group_id', db.Integer, db.ForeignKey('group.group_id')),
                   db.Column('course_id', db.Integer, db.ForeignKey('course.course_id')))


# user roles
class Role(db.Model):
    role_id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(10))

    def __repr__(self):
        return self.role_name


# student groups
class Group(db.Model):
    group_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    students = db.relationship('User',
                               secondary=groups,
                               lazy='subquery',
                               backref='group')
    courses = db.relationship('Course',
                              secondary=courses,
                              lazy='subquery',
                              backref='groups')

    def __repr__(self):
        """needed for correct caching"""
        return self.__class__.__name__ + self.name


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    _password = db.Column('password', db.String(100))
    role = db.Column(db.ForeignKey('role.role_id'))
    reports = db.relationship("Report")
    role_obj = db.relationship("Role")
    courses = db.relationship("Course")

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def check_password(self, password: str) ->bool:
        return sha256(password.encode()).hexdigest() == self._password

    def set_password(self, password: str) ->None:
        """
        doesn't commit changes to database, needs db.session.commit() after calling
        :param password: password string 
        :return: None
        """
        self._password = sha256(password.encode()).hexdigest()

    def __repr__(self):
        return self.name

    @property
    def password(self):
        return self._password


class Course(db.Model):  # course model
    course_id = db.Column(db.Integer(), primary_key=True)  # identifier
    course_name = db.Column(db.String(50), nullable=False)  # full name
    course_shortened = db.Column(db.String(10), nullable=False)  # shortened name (will be used in file paths)
    course_tutor = db.Column(db.Integer(), db.ForeignKey('user.id'), index=True)  # connecting to tutor
    labs_amount = db.Column(db.Integer(), nullable=False)   # amount of reports
    lab_max_score = db.Column(db.Integer(), nullable=False)  # max score for one lab
    course_tutor_obj = db.relationship("User")

    def __repr__(self):
        return '{} - {}'.format(self.course_name, self.course_shortened)


class Report(db.Model):
    report_id = db.Column(db.Integer(), primary_key=True)  # identifier
    report_course = db.Column(db.Integer(), db.ForeignKey('course.course_id'), index=True)  # course
    report_student = db.Column(db.Integer(), db.ForeignKey('user.id'), index=True)  # report owner
    report_num = db.Column(db.Integer(), nullable=False)
    report_mark = db.Column(db.Integer())   # mark for report
    report_uploaded = db.Column(db.DateTime(), nullable=False)   # upload time
    report_checked = db.Column(db.DateTime())  # check time
    report_stu_comment = db.Column(db.Text())  # comment of student
    report_tut_comment = db.Column(db.Text())  # comment of tutor
    report_hash = db.Column(db.String(32), nullable=False)   # checksum
    student_obj = db.relationship("User")

    def __repr__(self):
        return "Report id:{} course {} №{}".format(self.report_id,
                                         self.report_course,
                                         self.report_num,)
