"""Tests main conftest file."""
import warnings

import pytest_redis.factories.client
import pytest_redis.factories.noproc
import pytest_redis.factories.proc
from pytest_redis.plugin import *  # noqa: F403

warnings.filterwarnings(
    "error", category=DeprecationWarning, module="(_pytest|pytest|redis|path|mirakuru).*"
)

# pylint:disable=invalid-name
redis_proc2 = pytest_redis.factories.proc.redis_proc(port=6381)
redis_nooproc2 = pytest_redis.factories.noproc.redis_noproc(port=6381, startup_timeout=1)
redis_proc3 = pytest_redis.factories.proc.redis_proc(port=6385, password="secretpassword")
redis_nooproc3 = pytest_redis.factories.noproc.redis_noproc(port=6385, password="secretpassword")

redisdb2 = pytest_redis.factories.client.redisdb("redis_proc2")
redisdb2_noop = pytest_redis.factories.client.redisdb("redis_nooproc2")
redisdb3 = pytest_redis.factories.client.redisdb("redis_proc3")
redisdb3_noop = pytest_redis.factories.client.redisdb("redis_nooproc3")
# pylint:enable=invalid-name
