from labs_web.config import Config, NonDockerConfig
import redis
redis_conn = redis.StrictRedis(host=Config.CACHE_REDIS_HOST,
                               port=Config.CACHE_REDIS_PORT,
                               db=Config.REDIS_STRICT_CONNS_DB)
