from smtplib import SMTP_SSL
from redis import StrictRedis
from sqlalchemy import create_engine
from labs_web import NonDockerConfig


def test_db():
    """Deprecated, Unmaintained"""
    engine = create_engine(NonDockerConfig.SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    connection.close()


def test_redis():
    """Deprecated, Unmaintained"""
    redis = StrictRedis(host='localhost')
    redis.set('test', 'test')
    redis.get('test')


def test_smtp():
    """Deprecated, Unmaintained"""
    connection = SMTP_SSL(host=NonDockerConfig.MAIL_SERVER, port=NonDockerConfig.MAIL_PORT)
    connection.login(NonDockerConfig.MAIL_USERNAME, NonDockerConfig.MAIL_PASSWORD)
    assert connection.noop()[0] == 250  # success response


if __name__ == '__main__':
    test_db()
    test_redis()
    test_smtp()
