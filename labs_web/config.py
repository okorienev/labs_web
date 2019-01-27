import os


class Config(object):
    """Main config of application user to launch a dev server with docker-compose
Poor tested on uploaded & sending files"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alex:alex@postgres/labs_by_web_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_TIMEOUT = 5
    CSRF_ENABLED = True
    SECRET_KEY = 'e9fc4fca2c9fb29090742ad630e417bb5db210c9951f2420478ababd'
    UPLOAD_PATH = os.environ.get('UPLOADS_PATH')
    DOCS_FOLDER = os.environ.get('UPLOADS_PATH')
    TEST_DATA = os.environ.get('TEST_DATA')
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 60 * 60
    CACHE_KEY_PREFIX = 'labs_web'
    CACHE_REDIS_HOST = 'redis'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_URL = 'redis://redis:6379'
    REDIS_STRICT_CONNS_DB = 2
    DEBUG_TB_ENABLED = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    SQLALCHEMY_RECORD_QUERIES = True
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_SUPPRESS_SEND = True
    CELERY_IMPORTS = ('labs_web.views.tutor.check_reports',
                      'labs_web.views.tutor.ajax.check_reports_menu_ajax',
                      'labs_web.views.student.group_stats_in_course',
                      'labs_web.views.student.ajax.student_event_collector',
                      'labs_web.views.student.ajax.get_announcements_ajax',
                      'labs_web.views.tutor.ajax.get_tutor_announcements',
                      'labs_web.views.tutor.course_snapshot')
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password'
    ADMIN_EMAIL = 'admin@domain.com'
    MONGO_URL = 'mongodb'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'admin'
    MONGO_PASSWORD = 'password'


class NonDockerConfig(Config):
    """created to test on local machine with all infrastructure already installed
    to change check:
    labs_web/app.py (config importing) 
    and labs_web/extensions.extensions.py (celery instance creation)"""
    UPLOAD_PATH = '/home/alex/Dropbox/labs_web/labs_web/uploads/'
    TEST_DATA = '/home/alex/Dropbox/labs_web/labs_web/test_data/'
    DOCS_FOLDER = 'course_docs'
    CACHE_REDIS_URL = 'redis://localhost:6379'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alex:alex@localhost/labs_by_web_db'

