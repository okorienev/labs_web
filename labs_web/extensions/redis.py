from labs_web.config import Config, NonDockerConfig
import redis
from typing import Optional
from flask import current_app
from warnings import warn
redis_conn = redis.StrictRedis(host=Config.CACHE_REDIS_HOST,
                               port=Config.CACHE_REDIS_PORT,
                               db=Config.REDIS_STRICT_CONNS_DB)


def redis_get_int_or_none(key: str) -> Optional[int]:
    """
    wrap to avoid try/except boilerplate code for byte->int casts when working with redis responses
    :param key:
    :return: integer value or None if key is not present/can't be casted to int. In second case also writes error in log
    if any casting error was raised(TypeError, ValueError), writes a message to current app log if working in application
    context, warns with warnings.warn() otherwise
    """
    val = redis_conn.get(key)
    if val:
        try:
            val = int(val)
            return val
        except (TypeError, ValueError):
            template = f"Error casting value from redis to int: {val} can't be casted"
            if current_app:
                current_app.logger.error(template)
            else:
                warn(template)
    return None
