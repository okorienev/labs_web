class Config(object):
    debug = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alex:alex@localhost:5432/labs_by_web_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True
    SECRET_KEY = 'e9fc4fca2c9fb29090742ad630e417bb5db210c9951f2420478ababd'
    UPLOAD_PATH = '/home/alex/Dropbox/labs_web/uploads/'
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    CACHE_TYPE = 'simple'  # stub to check caching's work
    CACHE_DEFAULT_TIMEOUT = 60 * 60
    CACHE_KEY_PREFIX = 'labs_web',
    CACHE_REDIS_HOST = 'localhost',
    CACHE_REDIS_PORT = '6379',
    CACHE_REDIS_URL = 'redis://localhost:6379',
    DEBUG_TB_ENABLED = True

