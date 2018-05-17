from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery
from flask_caching import Cache
from flask_script import Manager

db = SQLAlchemy()
login_manager = LoginManager()
celery = Celery()
cache = Cache()
manager = Manager()
