from smtplib import SMTP_SSL
from redis import StrictRedis
from sqlalchemy import create_engine
from labs_web import Config


def test_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    connection.close()


def test_redis():
    redis = StrictRedis(host='localhost')
    redis.set('test', 'test')
    redis.get('test')


def test_smtp():
    connection = SMTP_SSL(host=Config.MAIL_SERVER, port=Config.MAIL_PORT)
    connection.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
    assert connection.noop()[0] == 250  # success response


if __name__ == '__main__':
    test_db()
    test_redis()
    test_smtp()
