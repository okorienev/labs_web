from flask import Flask, redirect, url_for, current_app, render_template
from .config import Config, NonDockerConfig
from flask_debugtoolbar import DebugToolbarExtension
from .extensions import db, login_manager, cache, mail, celery, ckeditor, admin, Role, User, mongo, Course, Group
from flask_migrate import Migrate
from flask_login import current_user
from .test_data import tutors, c_first_word, c_second_word, c_third_word, groups
from random import choice, randint
import csv
import string


app = Flask(__name__)
app.config.from_object(NonDockerConfig)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
db.init_app(app)
debug = DebugToolbarExtension(app)
cache.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)
admin.init_app(app)
ckeditor.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


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


def create_groups_and_students():
    with open('students.csv') as file:
        reader = csv.reader(file)
        iterator = iter(reader)
        for i in groups:
            group = Group(name=i)
            for i in range(30):
                row = next(iterator)

    pass


def create_reports():
    pass


def fill_db():
    """function to fill database with test data"""
    create_tutors_and_courses()


@app.before_first_request
def heavy_lifting():
    if not Role.query.first():
        create_db_and_roles()
    if not Course.query.first():
        fill_db()


@app.errorhandler(404)
def handle_404(*args, **kwargs):
    if current_user.is_authenticated:
        if current_user.role == 1:
            return render_template('student/student_404.html'), 404
        else:
            return render_template('tutor/tutor_404.html'), 404
    return render_template('errors/404_for_unauthorized.html'), 404


@app.route('/')
def hello_world():
    return redirect(url_for('auth.login'))
