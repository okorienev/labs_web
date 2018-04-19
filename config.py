class Config(object):
    debug = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alex:alex@localhost:5432/labs_by_web_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True
    SECRET_KEY = 'e9fc4fca2c9fb29090742ad630e417bb5db210c9951f2420478ababd'
    UPLOAD_PATH = '/home/alex/Dropbox/labs_web/uploads/'
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
