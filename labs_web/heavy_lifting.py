from flask import current_app
from .extensions import db, Role, User, Course, Group, Report
from labs_web.test_data import tutors, c_first_word, c_second_word, c_third_word, test_groups, students
from random import choice, randint
import os.path as p
import os
import datetime
import shutil
import hashlib


def create_uploads_folder():
    try:
        os.makedirs(current_app.config['UPLOAD_PATH'], exist_ok=True)
        os.mkdir(p.join(current_app.config['UPLOAD_PATH'],
                        current_app.config['DOCS_FOLDER']))
        os.mkdir(p.join(current_app.config['UPLOAD_PATH'],
                        'snapshots'))
    except FileExistsError:
        pass


def create_db_and_roles():
    """
    create db -> create user roles -> create admin user
    """
    db.create_all()
    roles = Role.query.all()
    if not roles:  # app has 3 roles for now
        student_role = Role(role_name='student')  # 3 db commits to be sure the roles got the correct identifiers
        db.session.add(student_role)
        db.session.commit()
        tutor_role = Role(role_name='tutor')
        db.session.add(tutor_role)
        db.session.commit()
        admin_role = Role(role_name='admin')
        db.session.add(admin_role)
        db.session.commit()
        assert Role.query.filter(Role.role_name == 'student').first().role_id == 1
        assert Role.query.filter(Role.role_name == 'tutor').first().role_id == 2
        assert Role.query.filter(Role.role_name == 'admin').first().role_id == 3
    admin_usr = User.query.filter(User.username == current_app.config.get("ADMIN_USERNAME")).first()
    if not admin_usr:
        admin_usr = User(username=current_app.config.get("ADMIN_USERNAME"),
                         email=current_app.config.get("ADMIN_EMAIL"),
                         name='ADMIN',
                         active=True,
                         role=3)
        admin_usr.set_password(current_app.config.get("ADMIN_PASSWORD"))
        db.session.add(admin_usr)
        db.session.commit()
    if not admin_usr.check_password(current_app.config.get("ADMIN_PASSWORD")):
        admin_usr.set_password(current_app.config.get("ADMIN_PASSWORD"))
        db.session.commit()


def random_course_name():
    """
    Generating random name and shortened for course. Check test_data.py to see variants of words to generate name from
    :return: tuple (course_name, course_shortened)
    e.g. course name is "Computer Methods of Integrating" and shortened will be "CMoI"
    """
    name = " ".join([choice(c_first_word),
                     choice(c_second_word),
                     "of",
                     choice(c_third_word)])
    shortened = "".join(map(lambda s: s[0], name.split()))
    return name, shortened


def create_tutors_and_courses():
    """
    creating tutors & courses for testing purposes
    30 tutors (data in test_data/test_data.tutors)
    creating 2 courses for each tutor
    see random_course_name() for details of random course name generating
    """
    for i in tutors:
        tutor = User(name=i[0], username=i[1], email=i[2], role=2)
        tutor.set_password('password')
        course_1_name = random_course_name()
        course_2_name = random_course_name()
        #
        course_1 = Course(course_name=course_1_name[0],
                          course_shortened=course_1_name[1],
                          course_tutor=tutor,
                          labs_amount=randint(3, 7),
                          lab_max_score=choice([5, 10, 20]))
        course_2 = Course(course_name=course_2_name[0],
                          course_shortened=course_2_name[1],
                          course_tutor=tutor,
                          labs_amount=randint(3, 7),
                          lab_max_score=choice([5, 10, 20]))
        tutor.courses.append(course_1)
        tutor.courses.append(course_2)
        #
        db.session.add(tutor)
        db.session.add(course_1)
        db.session.add(course_2)
        db.session.commit()
        #
        course_1 = Course.query.filter(Course.course_shortened == course_1_name[1]).first()
        course_1.course_shortened = "{}#{}".format(course_1.course_shortened,
                                                   course_1.course_id)
        course_2 = Course.query.filter(Course.course_shortened == course_2_name[1]).first()
        course_2.course_shortened = "{}#{}".format(course_2.course_shortened,
                                                   course_2.course_id)
        db.session.commit()
        #
        src = p.join(current_app.config['TEST_DATA'], 'example_docs.zip')
        dst = p.join(current_app.config['UPLOAD_PATH'], current_app.config['DOCS_FOLDER'], "{}.zip")
        shutil.copy(src, dst.format(course_1.course_shortened))
        shutil.copy(src, dst.format(course_2.course_shortened))


def create_groups_and_students():
    """
    creating groups & students for testing purposes
    30 groups (test_data.test_data.groups)
    30 students into each group (test_data/students.csv)
    adding courses (from 4 to 7) to each group
    """
    iterator = iter(students)
    for i in test_groups:
        group = Group(name=i)
        db.session.add(group)
        for i in range(30):
            row = next(iterator)
            student = User(name=row[0],
                           email=row[1],
                           username=row[2],
                           role=1)
            student.set_password('password')
            db.session.add(student)
            group.students.append(student)
    db.session.commit()
    groups = Group.query.all()
    courses = Course.query.all()
    for group in groups:
        for i in range(randint(4, 7)):
            group.courses.append(choice(courses))
    db.session.commit()


def create_reports():
    with open(p.join(current_app.config['TEST_DATA'], 'example_report.pdf'), 'rb') as file:
        file_hash = hashlib.md5(file.read()).hexdigest()
    courses = Course.query.all()
    for course in courses:
        for group in course.groups:
            for student in group.students:
                dirname = p.join(current_app.config['UPLOAD_PATH'],  # directory with reports of given student in a given course
                                 course.course_shortened,
                                 group.name,
                                 str(student.id))
                os.makedirs(dirname)
                for i in range(1, course.labs_amount, 2):
                    checked = choice((True, False))
                    report = Report(
                        report_course=course.course_id,
                        report_student=student.id,
                        report_num=i,
                        report_hash=file_hash,
                        report_uploaded=datetime.datetime.utcnow())
                    if checked:
                        report.report_checked = datetime.datetime.utcnow()
                        report.report_mark = randint(round(course.lab_max_score / 2), course.lab_max_score)
                    db.session.add(report)
                    shutil.copy(p.join(current_app.config['TEST_DATA'], 'example_report.pdf'), p.join(dirname,
                                                                                              str(report.report_num)))
    db.session.commit()


def fill_db():
    """function to fill database with test data"""
    if not Course.query.first():
        create_tutors_and_courses()
    if not Group.query.first():
        create_groups_and_students()
    if not Report.query.first():
        create_reports()