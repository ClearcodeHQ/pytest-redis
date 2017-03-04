"""Clean executor's tests."""
import pytest
import redis

from pytest_redis.executor import RedisExecutor
from pytest_redis.factories import get_config
from pytest_redis.port import get_port


@pytest.mark.parametrize('parameter, config_option, value', (
    ({'save': '900 1 300 10'}, 'save', '900 1 300 10'),
    ({'save': '900 1'}, 'save', '900 1'),
    ({'rdbcompression': True}, 'rdbcompression', 'yes'),
    ({'rdbcompression': False}, 'rdbcompression', 'no'),
    ({'rdbchecksum': True}, 'rdbchecksum', 'yes'),
    ({'rdbchecksum': False}, 'rdbchecksum', 'no'),

))
def test_redis_exec_configuration(request, parameter, config_option, value):
    """
    Check if RedisExecutor properly processes configuration options.

    Improperly set options won't be set in redis,
    and we won't be able to read it out of redis.
    """
    config = get_config(request)
    redis_exec = RedisExecutor(
        executable=config['exec'],
        databases=4,
        redis_timeout=config['timeout'],
        loglevel=config['loglevel'],
        logsdir=config['logsdir'],
        port=get_port(None),
        host=config['host'],
        timeout=30,
        **parameter
    )
    with redis_exec:
        redis_client = redis.StrictRedis(
            redis_exec.host, redis_exec.port, 0
        )
        assert redis_client.config_get(config_option) == {config_option: value}


@pytest.mark.parametrize('value, redis_value', (
    (True, 'yes'),
    (1, 'yes'),
    ('str', 'yes'),
    ('yes', 'yes'),
    (False, 'no'),
    (0, 'no'),
    ('', 'no'),
    ('no', 'no'),
))
def test_convert_bool(value, redis_value):
    """Check correctness of the redis_bool method."""
    assert RedisExecutor._redis_bool(value) == redis_value
