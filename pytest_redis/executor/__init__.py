"""Redis executor."""

from pytest_redis.executor.process import RedisExecutor
from pytest_redis.executor.noop import NoopRedis

__all__ = ("RedisExecutor", "NoopRedis")
