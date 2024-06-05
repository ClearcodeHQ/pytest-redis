"""Redis process fixture factory."""

from pathlib import Path
from typing import Callable, Generator, List, Optional, Set, Tuple, Union

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory
from port_for import get_port

from pytest_redis.config import get_config
from pytest_redis.executor import RedisExecutor


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
    modules: Optional[List[str]] = None,
) -> Callable[[FixtureRequest, TempPathFactory], Generator[RedisExecutor, None, None]]:
    """Fixture factory for pytest-redis.

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
    :param modules: list of paths of Redis extension modules to load
    :returns: function which makes a redis process
    """

    @pytest.fixture(scope="session")
    def redis_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Generator[RedisExecutor, None, None]:
        """Fixture for pytest-redis.

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

        redis_modules = modules or config["modules"]

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
            modules=redis_modules,
        )
        with redis_executor:
            yield redis_executor

    return redis_proc_fixture
