from flask import Flask, Blueprint, render_template, redirect, url_for, request, g
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import *
from config import Config
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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
        pass
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
    return 'hello world'

if __name__ == '__main__':
    # db.create_all()
    app.register_blueprint(auth)
    app.run()
