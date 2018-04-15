# TODO clean all the rubbish, make normal project structure
# TODO end sending report
# TODO create some representative templates for tutor/student home pages
# TODO test test test

from werkzeug.utils import secure_filename
from flask import Flask, Blueprint, render_template, redirect, url_for, request, g, flash, abort
from flask_login import LoginManager, current_user, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from config import Config
from forms import LoginForm, ReportSendingForm
from models import *
from os.path import join

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = SQLAlchemy()
db.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


#
# authentication blueprint
#
auth = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        remember_me = request.form.get('remember_me')
        user = User.query.filter_by(username=username).first()
        if user.check_password(password) and ((user.role == 1 and user_type == 'student') or
                                                          user.role == 2 and user_type == 'tutor'):
            login_user(user, remember=remember_me)
            if user.role == 1:
                return redirect(url_for('student.give_report'))
            if user.role == 2:
                return redirect(url_for('tutor.home'))
        else:
            return abort(403)
    return render_template('login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    return 'i am logout page'


#
# authentication blueprint end
#

#
# student views blueprint
#
student = Blueprint('student',
                    __name__,
                    url_prefix='/student')


@student.route('/report/', methods=['GET', 'POST'])
@login_required
def give_report():
    form = ReportSendingForm()
    query = text("SELECT course_shortened, course_name, labs_amount "
                 "FROM "
                 "(SELECT course_id, user_id "
                 "FROM group_courses "
                 "JOIN user_groups "
                 "ON group_courses.group_id = user_groups.group_id) as g "
                 "JOIN course ON g.course_id = course.course_id "
                 "WHERE user_id = :user_id"
                 )
    courses_of_user = [{'name': i.course_name, 'shortened': i.course_shortened}
                       for i in db.engine.execute(query, user_id=current_user.id)]
    if request.method == 'POST' and form.validate_on_submit():

        list_of_shortened = [i['shortened'] for i in courses_of_user]
        print(list_of_shortened)

        if request.form.get('course') not in list_of_shortened:  # user's group should have this course
            flash('You don\'t have this course')
            return redirect(request.url)
        query = text("""SELECT course.labs_amount FROM course WHERE course_shortened = :shortened""")
        lab_max_amount = [i['labs_amount'] for i in db.engine.execute(query, shortened=request.form.get('course'))]

        if request.form.get('number_in_course') < 1 or request.form.get('number_in_course') > lab_max_amount:
            flash('lab number out of range')  # lab number should be in range between 1 and max lab number in course
            return redirect(request.url)

        if 'file' not in request.files:
            flash('file was not chosen')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('no file selected')
            return redirect(request.url)

        if file and (lambda filename: '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf')(file.filename):
            filename = secure_filename(file.filename)
            query = text("""SELECT "group".name
                            FROM user_groups
                            JOIN "group" ON user_groups.group_id = "group".group_id
                            WHERE user_id = :user_id""")
            group = [i.name for i in db.engine.execute(query, user_id=current_user.id)]
            print(group)
            file.save(join(app.config['UPLOAD_FOLDER'],
                           (request.form.get('course'),
                            group,
                            current_user.id,
                            filename)))
        print(request.form.get('course'), request.form.get('number_in_course'), request.form.get('comment'))
    return render_template('give_report.html', user=current_user, form=form, courses=courses_of_user)


#
# student views end
#

#
# tutor views blueprint
#
tutor = Blueprint('tutor',
                  __name__,
                  url_prefix='/tutor')


@tutor.route('/home/')
@login_required
def tutor_home():
    return render_template('tutor_home.html')


#
# tutor views end
#


@app.route('/')
def hello_world():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(tutor)
    app.run()
