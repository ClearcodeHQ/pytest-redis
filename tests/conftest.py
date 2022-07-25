"""Tests main conftest file."""
import warnings

from pytest_redis import factories

warnings.filterwarnings(
    "error", category=DeprecationWarning, module="(_pytest|pytest|redis|path|mirakuru).*"
)

# pylint:disable=invalid-name
redis_proc2 = factories.redis_proc(port=6381)
redis_nooproc2 = factories.redis_noproc(port=6381)
redis_proc3 = factories.redis_proc(port=6385, password="secretpassword")
redis_nooproc3 = factories.redis_noproc(port=6385, password="secretpassword")
redisdb2 = factories.redisdb("redis_proc2")
redisdb2_noop = factories.redisdb("redis_nooproc2")
redisdb3 = factories.redisdb("redis_proc3")
redisdb3_noop = factories.redisdb("redis_nooproc3")
# pylint:enable=invalid-name
