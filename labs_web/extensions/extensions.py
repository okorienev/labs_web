from alembic.util import immutabledict
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from flask_mail import Mail
from celery import Celery
from sqlalchemy import MetaData

from labs_web.config import Config, NonDockerConfig
from flask_admin import Admin
from flask_ckeditor import CKEditor
from pymongo import MongoClient

from labs_web.extensions.minio import MinioManager

naming_convention = immutabledict({
    'uq': '%(table_name)s_%(column_0_N_name)s_key',    # unique constraint
    'ix': '%(table_name)s_%(column_0_N_name)s_idx',    # index
    'pk': '%(table_name)s_pkey',                       # primary key
    'fk': '%(table_name)s_%(column_0_N_name)s_fkey',   # foreign key
    'ck': '%(table_name)s_%(column_0_N_name)s_check',  # check constraint
})
metadata = MetaData(naming_convention=naming_convention)

db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()
cache = Cache()
mail = Mail()
admin = Admin()
celery = Celery(broker=Config.CELERY_BROKER_URL)
celery.config_from_object(Config)
ckeditor = CKEditor()
mongo = MongoClient("mongodb://{}:{}@{}".format(Config.MONGO_USERNAME,
                                                Config.MONGO_PASSWORD,
                                                Config.MONGO_URL,
                                                Config.MONGO_PORT))

minio = MinioManager(Config.MINIO)
