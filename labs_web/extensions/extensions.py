from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from flask_mail import Mail
from celery import Celery
from labs_web.config import Config, NonDockerConfig
from flask_admin import Admin
from flask_ckeditor import CKEditor
from pymongo import MongoClient

db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache()
mail = Mail()
admin = Admin()
celery = Celery(broker=NonDockerConfig.CELERY_BROKER_URL)
celery.config_from_object(Config)
ckeditor = CKEditor()
mongo = MongoClient('localhost', 27017)
