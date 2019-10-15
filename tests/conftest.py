"""Tests main conftest file."""
import warnings

from pytest_redis import factories

warnings.filterwarnings(
    "error",
    category=DeprecationWarning,
    module='(_pytest|pytest|redis|path|mirakuru).*'
)

# pylint:disable=invalid-name
redis_proc2 = factories.redis_proc(port=6381)
redis_nooproc2 = factories.redis_proc(port=6381)
redisdb2 = factories.redisdb('redis_proc2')
redisdb2_noop = factories.redisdb('redis_nooproc2')
# pylint:enable=invalid-name
