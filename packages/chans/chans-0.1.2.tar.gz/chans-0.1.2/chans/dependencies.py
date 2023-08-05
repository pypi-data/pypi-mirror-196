import contextlib
import os

from redis import Redis
from redis.asyncio import Redis as RedisAsync

def get_redis():
    r = Redis.from_url(os.environ['REDIS_URL'], decode_responses=True)
    yield r
    r.close()

def get_redis_async():
    r = RedisAsync.from_url(os.environ['REDIS_URL'], decode_responses=True)
    yield r
    r.close()

get_redis_cm = contextlib.contextmanager(get_redis)
get_redis_async_cm = contextlib.contextmanager(get_redis_async)
