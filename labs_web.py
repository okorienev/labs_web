from flask import Flask, redirect, url_for
from config import Config
from extensions.extensions import login_manager, cache, mail, celery
from flask_debugtoolbar import DebugToolbarExtension
from extensions.models import db, User
from views.auth.auth_main import auth
from views.student.student_main import student
from views.tutor.tutor_main import tutor
from views.admin.admin_main import admin
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
db.init_app(app)
debug = DebugToolbarExtension(app)
cache.init_app(app)
migrate = Migrate(app, db)
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)
mail.init_app(app)


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
    app.register_blueprint(admin)
    app.run(debug=True)
