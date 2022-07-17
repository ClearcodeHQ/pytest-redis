"""Clean executor's tests."""
from io import StringIO

import socket
import pytest
import redis
from pkg_resources import parse_version
from pytest import FixtureRequest, TempPathFactory
from mock import mock
from port_for import get_port

from mirakuru.exceptions import TimeoutExpired
from pytest_redis.executor import (
    NoopRedis,
    RedisExecutor,
    RedisMisconfigured,
    extract_version,
    RedisUnsupported,
    UnixSocketTooLong,
)
from pytest_redis.factories import get_config


@pytest.mark.parametrize(
    "parameter, config_option, value",
    (
        ({"save": "900 1 300 10"}, "save", "900 1 300 10"),
        ({"save": "900 1"}, "save", "900 1"),
        ({"rdbcompression": True}, "rdbcompression", "yes"),
        ({"rdbcompression": False}, "rdbcompression", "no"),
        ({"rdbchecksum": True}, "rdbchecksum", "yes"),
        ({"rdbchecksum": False}, "rdbchecksum", "no"),
    ),
)
def test_redis_exec_configuration(
    request: FixtureRequest, tmp_path_factory: TempPathFactory, parameter, config_option, value
):
    """
    Check if RedisExecutor properly processes configuration options.

    Improperly set options won't be set in redis,
    and we won't be able to read it out of redis.
    """
    config = get_config(request)
    tmpdir = tmp_path_factory.mktemp(f"pytest-redis-test-test_redis_exec_configuration")
    redis_exec = RedisExecutor(
        executable=config["exec"],
        databases=4,
        redis_timeout=config["timeout"],
        loglevel=config["loglevel"],
        port=get_port(None),
        host=config["host"],
        timeout=30,
        datadir=tmpdir,
        **parameter,
    )
    with redis_exec:
        redis_client = redis.StrictRedis(redis_exec.host, redis_exec.port, 0)
        assert redis_client.config_get(config_option) == {config_option: value}


@pytest.mark.parametrize(
    "parameter",
    (
        {"syslog_enabled": True},
        {"syslog_enabled": False},
    ),
)
def test_redis_exec(request: FixtureRequest, tmp_path_factory: TempPathFactory, parameter):
    """
    Check if RedisExecutor properly starts with these configuration options.

    Incorrect options won't even start redis.
    """
    config = get_config(request)
    tmpdir = tmp_path_factory.mktemp(f"pytest-redis-test-test_redis_exec")
    redis_exec = RedisExecutor(
        executable=config["exec"],
        databases=4,
        redis_timeout=config["timeout"],
        loglevel=config["loglevel"],
        port=get_port(None),
        host=config["host"],
        timeout=30,
        datadir=tmpdir,
        **parameter,
    )
    with redis_exec:
        assert redis_exec.running()


@pytest.mark.parametrize(
    "value, redis_value",
    (
        (True, "yes"),
        (1, "yes"),
        ("str", "yes"),
        ("yes", "yes"),
        (False, "no"),
        (0, "no"),
        ("", "no"),
        ("no", "no"),
    ),
)
def test_convert_bool(value, redis_value):
    """Check correctness of the redis_bool method."""
    # pylint:disable=protected-access
    assert RedisExecutor._redis_bool(value) == redis_value
    # pylint:enable=protected-access


@pytest.mark.parametrize(
    "version",
    (
        "Redis server version 2.4.14 (e9935407:0)",
        "Redis server version 2.4.13 (e0935407:0)"
        "Redis server version 2.5.0 (e9035407:0)"
        "Redis server version 2.3.10 (e9933407:0)",
    ),
)
def test_old_redis_version(request: FixtureRequest, tmp_path_factory: TempPathFactory, version):
    """Test how fixture behaves in case of old redis version."""
    config = get_config(request)
    tmpdir = tmp_path_factory.mktemp(f"pytest-redis-test-test_old_redis_version")
    with mock.patch("os.popen", lambda *args: StringIO(version)):
        with pytest.raises(RedisUnsupported):
            RedisExecutor(
                config["exec"],
                databases=4,
                redis_timeout=config["timeout"],
                loglevel=config["loglevel"],
                port=get_port(None),
                host=config["host"],
                timeout=30,
                datadir=tmpdir,
            ).start()


def test_not_existing_redis(request: FixtureRequest, tmp_path_factory: TempPathFactory):
    """Check handling of misconfigured redis executable path."""
    config = get_config(request)
    tmpdir = tmp_path_factory.mktemp(f"pytest-redis-test-test_not_existing_redis")
    with pytest.raises(RedisMisconfigured):
        RedisExecutor(
            "/not/redis/here/redis-server",
            databases=4,
            redis_timeout=config["timeout"],
            loglevel=config["loglevel"],
            port=get_port(None),
            host=config["host"],
            timeout=30,
            datadir=tmpdir,
        ).start()


def test_too_long_unixsocket(request: FixtureRequest, tmp_path_factory: TempPathFactory):
    """Check handling of misconfigured redis executable path."""
    config = get_config(request)
    tmpdir = tmp_path_factory.mktemp(f"x" * 110)
    with pytest.raises(UnixSocketTooLong):
        RedisExecutor(
            config["exec"],
            databases=4,
            redis_timeout=config["timeout"],
            loglevel=config["loglevel"],
            port=get_port(None),
            host=config["host"],
            timeout=30,
            datadir=tmpdir,
        ).start()


@pytest.mark.parametrize(
    "text,result",
    [
        ("Redis server version 2.4.14 (00000000:0)", "2.4.14"),
        ("Redis server v=2.6.13 sha=00000000:0 malloc=jemalloc-3.3.1 bits=64", "2.6.13"),
        ("1.2.5", "1.2.5"),
        ("Test2.0.5", "2.0.5"),
        ("2.0.5Test", "2.0.5"),
        ("m.n.a 2.4.14", "2.4.14"),
    ],
)
def test_extract_version(text, result):
    """Check if the version extracction works correctly."""
    assert extract_version(text) == parse_version(result)


def test_extract_version_notfound():
    with pytest.raises(AssertionError):
        extract_version("Test")


def test_noopredis_handles_timeout_when_waiting():
    with mock.patch('pytest_redis.executor.socket', spec=socket) as patched_socket:
        foo = patched_socket.socket.return_value
        socket_mock = foo.__enter__.return_value
        socket_mock.connect.side_effect = TimeoutError()
        noop_redis = NoopRedis('localhost', 12345, None, timeout=1)
        with pytest.raises(TimeoutExpired):
            noop_redis.start()

        assert not noop_redis.running()
        socket_mock.settimeout.assert_called_with(0.1)
        socket_mock.connect.assert_called()
