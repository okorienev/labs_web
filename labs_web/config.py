class Config(object):
    debug = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alex:alex@localhost:5432/labs_by_web_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_TIMEOUT = 5
    CSRF_ENABLED = True
    SECRET_KEY = 'e9fc4fca2c9fb29090742ad630e417bb5db210c9951f2420478ababd'
    UPLOAD_PATH = '/home/alex/Dropbox/labs_web/labs_web/uploads/'
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 60 * 60
    CACHE_KEY_PREFIX = 'labs_web'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_URL = 'redis://localhost:6379'
    DEBUG_TB_ENABLED = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    CELERY_IMPORTS = ('labs_web.views.tutor.check_reports',
                      'labs_web.views.tutor.check_reports_menu_ajax',
                      'labs_web.views.student.group_stats_in_course',
                      'labs_web.views.student.student_event_collector')
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'password'
    ADMIN_EMAIL = 'admin@domain.com'


