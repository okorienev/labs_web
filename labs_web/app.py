from flask import Flask, redirect, url_for, render_template, abort
from .config import Config
from flask_debugtoolbar import DebugToolbarExtension
from .extensions import db, login_manager, cache, mail, ckeditor, admin, celery, User
from flask_migrate import Migrate
from flask_login import current_user
from .heavy_lifting import *
from logging import getLogger

app = Flask(__name__)
app.config.from_object(Config)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
db.init_app(app)
debug = DebugToolbarExtension(app)
cache.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)
admin.init_app(app)
ckeditor.init_app(app)


logger = getLogger(__name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


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


@app.route('/_fill-db')
def fill_db():
    if app.config["DEBUG"]:
        create_db()
        create_tickets()
        create_announcements()
        return "Dummy init completed"
    else:
        logger.critical('Attempt to access view in non-debug mode')
        raise abort(404)
