from redis import Redis
from rest_framework import exceptions
from .settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB
)


try:
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
except redis.RedisError as exception:
    raise RedisKeyedVectorException(exception)