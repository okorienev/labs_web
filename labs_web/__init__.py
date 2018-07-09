from flask import Flask, redirect, url_for
from .config import Config
from .extensions import login_manager, cache, mail, celery
from flask_debugtoolbar import DebugToolbarExtension
from .extensions import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
db.init_app(app)
debug = DebugToolbarExtension(app)
cache.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def hello_world():
    return redirect(url_for('auth.login'))
