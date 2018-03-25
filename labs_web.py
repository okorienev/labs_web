from flask import Flask, Blueprint, render_template, redirect, url_for, request, g
from flask_login import LoginManager, current_user, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from config import Config
from forms import LoginForm
from models import *

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
        if user.check_password(password):
            login_user(user, remember=remember_me)
            print(current_user.username)
        return render_template('student_home.html', username=username,
                               password=password, user_type=user_type, remember_me=remember_me)
    return render_template('login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    return 'i am logout page'
#
# authentication blueprint end
#


@app.route('/')
def hello_world():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.register_blueprint(auth)
    app.run()
