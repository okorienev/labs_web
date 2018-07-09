from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from flask_mail import Mail
from celery import Celery
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache()
mail = Mail()
celery = Celery(broker=Config.CELERY_BROKER_URL)
celery.config_from_object(Config)

