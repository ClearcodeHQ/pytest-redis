# Copyright (C) 2013 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-redis.

# pytest-redis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-redis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-redis.  If not, see <http://www.gnu.org/licenses/>.
"""Fixture factories for pytest-redis."""
from pathlib import Path
from typing import TypedDict, Any, Optional, Tuple, Set, List, Union, Callable, Generator, Literal

import pytest
import redis
from pytest import TempPathFactory, FixtureRequest
from port_for import get_port

from pytest_redis.executor import RedisExecutor, NoopRedis


class RedisConfigType(TypedDict):
    host: str
    port: Optional[int]
    username: str
    password: str
    exec: str
    timeout: int
    loglevel: str
    db_count: int
    save: str
    compression: bool
    rdbchecksum: bool
    syslog: bool
    decode: bool
    datadir: str


def get_config(request: FixtureRequest) -> RedisConfigType:
    """Return a dictionary with config options."""

    def get_conf_option(option: str) -> Any:
        option_name = "redis_" + option
        return request.config.getoption(option_name) or request.config.getini(option_name)

    port = get_conf_option("port")
    config: RedisConfigType = {
        "host": get_conf_option("host"),
        "port": int(port) if port else None,
        "username": get_conf_option("username"),
        "password": get_conf_option("password"),
        "exec": get_conf_option("exec"),
        "timeout": int(get_conf_option("timeout")),
        "loglevel": get_conf_option("loglevel"),
        "db_count": int(get_conf_option("db_count")),
        "save": get_conf_option("save"),
        "compression": bool(get_conf_option("compression")),
        "rdbchecksum": bool(get_conf_option("rdbchecksum")),
        "syslog": bool(get_conf_option("syslog")),
        "decode": bool(get_conf_option("decode")),
        "datadir": get_conf_option("datadir"),
    }
    return config


def redis_proc(
    executable: Optional[str] = None,
    timeout: Optional[int] = None,
    host: Optional[str] = None,
    port: Union[
        None,
        str,
        int,
        Tuple[int, int],
        Set[int],
        List[str],
        List[int],
        List[Tuple[int, int]],
        List[Set[int]],
        List[Union[Set[int], Tuple[int, int]]],
        List[Union[str, int, Tuple[int, int], Set[int]]],
    ] = -1,
    username: Optional[str] = None,
    password: Optional[str] = None,
    db_count: Optional[int] = None,
    save: Optional[str] = None,
    compression: Optional[bool] = None,
    checksum: Optional[bool] = None,
    syslog: Optional[bool] = None,
    loglevel: Optional[str] = None,
    datadir: Optional[str] = None,
) -> Callable[[FixtureRequest, TempPathFactory], Generator[RedisExecutor, None, None]]:
    """
    Fixture factory for pytest-redis.

    :param executable: path to redis-server
    :param timeout: client's connection timeout
    :param host: hostname
    :param port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given orange and set
    :param username: username
    :param password: password
    :param db_count: number of databases redis should have
    :param save: redis save configuration setting
    :param compression: Compress redis dump files
    :param checksum: Whether to add checksum to the rdb files
    :param syslog:Whether to enable logging to the system logger
    :param loglevel: redis log verbosity level.
        One of debug, verbose, notice or warning
    :param datadir: Path for redis data files, including the unix domain socket.
        If this is not configured, then a temporary directory is created and used
        instead.
    :returns: function which makes a redis process
    """

    @pytest.fixture(scope="session")
    def redis_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Generator[RedisExecutor, None, None]:
        """
        Fixture for pytest-redis.

        #. Get configs.
        #. Run redis process.
        #. Stop redis process after tests.

        :param request: fixture request object
        :param tmpdir_factory:
        :rtype: pytest_redis.executors.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        redis_exec = executable or config["exec"]
        rdbcompression: bool = config["compression"] if compression is None else compression
        rdbchecksum: bool = config["rdbchecksum"] if checksum is None else checksum

        if datadir:
            redis_datadir = Path(datadir)
        elif config["datadir"]:
            redis_datadir = Path(config["datadir"])
        else:
            redis_datadir = tmp_path_factory.mktemp(f"pytest-redis-{request.fixturename}")

        redis_port = get_port(port) or get_port(config["port"])
        assert redis_port
        redis_executor = RedisExecutor(
            executable=redis_exec,
            databases=db_count or config["db_count"],
            redis_timeout=timeout or config["timeout"],
            loglevel=loglevel or config["loglevel"],
            rdbcompression=rdbcompression,
            rdbchecksum=rdbchecksum,
            syslog_enabled=syslog or config["syslog"],
            save=save or config["save"],
            host=host or config["host"],
            port=redis_port,
            username=username or config["username"],
            password=password or config["password"],
            startup_timeout=60,
            datadir=redis_datadir,
        )
        with redis_executor:
            yield redis_executor

    return redis_proc_fixture


def redis_noproc(
    host: Optional[str] = None,
    port: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    startup_timeout: int = 15,
) -> Callable[[FixtureRequest], Generator[NoopRedis, None, None]]:
    """
    Nooproc fixture factory for pytest-redis.

    :param host: hostname
    :param port: exact port (e.g. '8000', 8000)
    :param username: username used for authentication
    :param password: password used for authentication
    :param startup_timeout: Blocking wait until we give up connecting to Redis.
    :returns: function which makes a redis process
    """

    @pytest.fixture(scope="session")
    def redis_nooproc_fixture(request: FixtureRequest) -> Generator[NoopRedis, None, None]:
        """
        Nooproc fixture for pytest-redis.

        Builds mock executor to run tests with

        :param FixtureRequest request: fixture request object
        :rtype: pytest_redis.executors.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        redis_noopexecutor = NoopRedis(
            host=host or config["host"],
            port=port or config["port"] or 6379,
            username=username or config["username"],
            password=password or config["password"],
            unixsocket=None,
            startup_timeout=startup_timeout,
        )

        with redis_noopexecutor:
            yield redis_noopexecutor

    return redis_nooproc_fixture


def redisdb(
    process_fixture_name: str, dbnum: int = 0, decode: Optional[bool] = None
) -> Callable[[FixtureRequest], Generator[redis.Redis, None, None]]:
    """
    Create connection fixture factory for pytest-redis.

    :param process_fixture_name: name of the process fixture
    :param dbnum: number of database to use
    :param decode: Client: to decode response or not.
        See redis.StrictRedis decode_reponse client parameter.
    :returns: function which makes a connection to redis
    """

    @pytest.fixture
    def redisdb_factory(request: FixtureRequest) -> Generator[redis.Redis, None, None]:
        """
        Create connection for pytest-redis.

        #. Load required process fixture.
        #. Get redis module and config.
        #. Connect to redis.
        #. Flush database after tests.

        :param FixtureRequest request: fixture request object
        :rtype: redis.client.Redis
        :returns: Redis client
        """
        proc_fixture: Union[NoopRedis, RedisExecutor] = request.getfixturevalue(
            process_fixture_name
        )
        config = get_config(request)

        redis_host = proc_fixture.host
        redis_port = proc_fixture.port
        redis_username = proc_fixture.username
        redis_password = proc_fixture.password
        redis_db = dbnum
        decode_responses: Union[Literal[True], Literal[False]] = (
            decode if decode is not None else config["decode"]
        )

        redis_client = redis.Redis(
            redis_host,
            redis_port,
            redis_db,
            username=redis_username,
            password=redis_password,
            unix_socket_path=proc_fixture.unixsocket,
            decode_responses=decode_responses,
        )

        yield redis_client
        redis_client.flushall()

    return redisdb_factory


__all__ = ("redisdb", "redis_proc")
