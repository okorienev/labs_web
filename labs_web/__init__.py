from flask import Flask, redirect, url_for
from .config import Config, NonDockerConfig
from .extensions import login_manager, cache, mail, celery, admin, Role, User
from flask_debugtoolbar import DebugToolbarExtension
from .extensions import db, User
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(NonDockerConfig)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
db.init_app(app)
debug = DebugToolbarExtension(app)
cache.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)
admin.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_first_request
def create_db_and_roles():
    """
    create db -> create user roles -> create admin user
    """
    db.create_all()
    roles = Role.query.all()
    if not roles:  # app has 3 roles for now
        student_role = Role(role_name='student')   # 3 db commits to be sure the roles got the correct identifiers
        db.session.add(student_role)
        db.session.commit()
        tutor_role = Role(role_name='tutor')
        db.session.add(tutor_role)
        db.session.commit()
        admin_role = Role(role_name='admin')
        db.session.add(admin_role)
        db.session.commit()
        assert Role.query.filter(Role.role_name == 'student').first().role_id == 1
        assert Role.query.filter(Role.role_name == 'tutor').first().role_id == 2
        assert Role.query.filter(Role.role_name == 'admin').first().role_id == 3
    admin_usr = User.query.filter(User.username == Config.ADMIN_USERNAME).first()
    if not admin_usr:
        admin_usr = User(username=Config.ADMIN_USERNAME,
                         email=Config.ADMIN_EMAIL,
                         name='ADMIN',
                         active=True,
                         role=3)
        admin_usr.set_password(Config.ADMIN_PASSWORD)
        db.session.add(admin_usr)
        db.session.commit()
    if not admin_usr.check_password(Config.ADMIN_PASSWORD):
        admin_usr.set_password(Config.ADMIN_PASSWORD)
        db.session.commit()


@app.route('/')
def hello_world():
    return redirect(url_for('auth.login'))
