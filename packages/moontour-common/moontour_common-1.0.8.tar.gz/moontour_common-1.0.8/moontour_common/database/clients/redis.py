import os
import redis

host = os.getenv('REDIS_HOST', 'redis')
redis_client = redis.Redis(host=host)
