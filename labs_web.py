from flask import Flask, redirect, url_for
from config import Config
from extensions.extensions import login_manager
from flask_debugtoolbar import DebugToolbarExtension
from extensions.models import db, User
from views.auth.auth_main import auth
from views.student.student_main import student
from views.tutor.tutor_main import tutor

app = Flask(__name__)
app.config.from_object(Config)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
db.init_app(app)
debug = DebugToolbarExtension(app)


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
    app.run(debug=True)
