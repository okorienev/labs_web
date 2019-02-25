from flask import Flask, redirect, url_for, render_template
from .config import NonDockerConfig, Config
from flask_debugtoolbar import DebugToolbarExtension
from .extensions import db, login_manager, cache, mail, ckeditor, admin, celery
from flask_migrate import Migrate
from flask_login import current_user
from .heavy_lifting import *

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


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_first_request
def heavy_lifting():
    create_uploads_folder()
    create_db_and_roles()
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
