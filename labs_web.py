# TODO clean all the rubbish, make normal project structure
# TODO end sending report
# TODO create some representative templates for tutor/student home pages
# TODO test test test

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, User
from views.auth.auth_main import auth
from views.student.student_main import student
from views.tutor.tutor_main import tutor

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db.init_app(app)
db.create_all(app=app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def hello_world():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(tutor)
    app.run()
