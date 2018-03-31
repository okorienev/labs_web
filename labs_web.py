# TODO clean all the rubbish, make normal project structure
# TODO end sending report
# TODO create some representative templates for tutor/student home pages
# TODO test test test

from flask import Flask, Blueprint, render_template, redirect, url_for, request, g
from flask_login import LoginManager, current_user, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from config import Config
from forms import LoginForm, ReportSendingForm
from models import *
from os import getcwd

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
        print(user.id, user.username, user.name, user.email, user.role)
        if user.check_password(password) and ((user.role == 1 and user_type == 'student') or
                                                user.role == 2 and user_type == 'tutor'):
            login_user(user, remember=remember_me)
            if user.role == 1:
                return redirect(url_for('student.home'))
            if user.role == 2:
                return redirect(url_for('tutor.home'))
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
    print(getcwd())
    with open('/home/alex/Dropbox/labs_web/SQL_raw_queries/shortened_course_name_by_user_id.sql') as f:
        query = f.read()
        courses = [(row['course_shortened'], row['course_shortened']) for row in db.engine.execute(query.format(current_user.id))]
    if request.method == 'POST':
        form = ReportSendingForm(courses)
    return render_template(give_report, user=current_user, form=form)
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
