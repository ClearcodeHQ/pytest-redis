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
"""FIxture factories for pytest-redis."""
import pytest
import redis

from pytest_redis.executor import RedisExecutor, NoopRedis
from pytest_redis.port import get_port


def get_config(request):
    """Return a dictionary with config options."""
    config = {}
    options = [
        'logsdir', 'host', 'port', 'exec', 'timeout', 'loglevel', 'db_count',
        'save', 'compression', 'rdbchecksum', 'syslog', 'decode'
    ]
    for option in options:
        option_name = 'redis_' + option
        conf = request.config.getoption(option_name) or \
            request.config.getini(option_name)
        config[option] = conf
    return config


def redis_proc(
        executable=None, timeout=None, host=None, port=-1, db_count=None,
        save=None, compression=None, checksum=None, syslog=None,
        logsdir=None, logs_prefix='', loglevel=None
):
    """
    Fixture factory for pytest-redis.

    :param str executable: path to redis-server
    :param int timeout: client's connection timeout
    :param str host: hostname
    :param str|int|tuple|set|list port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given orange and set
    :param int db_count: number of databases redis should have
    :param str save: redis save configuration setting
    :param bool compression: Compress redis dump files
    :param bool checksum: Whether to add checksum to the rdb files
    :param bool syslog:Whether to enable logging to the system logger
    :param str logsdir: path to log directory
    :param str logs_prefix: prefix for log filename
    :param str loglevel: redis log verbosity level.
        One of debug, verbose, notice or warning
    :rtype: func
    :returns: function which makes a redis process
    """
    @pytest.fixture(scope='session')
    def redis_proc_fixture(request):
        """
        Fixture for pytest-redis.

        #. Get configs.
        #. Run redis process.
        #. Stop redis process after tests.

        :param FixtureRequest request: fixture request object
        :rtype: pytest_redis.executors.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        redis_exec = executable or config['exec']
        rdbcompression = config['compression'] \
            if compression is None else compression
        rdbchecksum = config['rdbchecksum'] if checksum is None else checksum

        redis_executor = RedisExecutor(
            executable=redis_exec,
            databases=db_count or config['db_count'],
            redis_timeout=timeout or config['timeout'],
            loglevel=loglevel or config['loglevel'],
            logsdir=logsdir or config['logsdir'],
            logs_prefix=logs_prefix,
            rdbcompression=rdbcompression,
            rdbchecksum=rdbchecksum,
            syslog_enabled=syslog or config['syslog'],
            save=save or config['save'],
            host=host or config['host'],
            port=get_port(port) or get_port(config['port']),
            timeout=60,
        )
        redis_executor.start()
        request.addfinalizer(redis_executor.stop)

        return redis_executor

    return redis_proc_fixture


def redis_noproc(host=None, port=None):
    """
    Nooproc fixture factory for pytest-redis.

    :param str host: hostname
    :param str|int port: exact port (e.g. '8000', 8000)
    :rtype: func
    :returns: function which makes a redis process
    """
    @pytest.fixture(scope='session')
    def redis_nooproc_fixture(request):
        """
        Nooproc fixture for pytest-redis.

        Builds mock executor to run tests with

        :param FixtureRequest request: fixture request object
        :rtype: pytest_redis.executors.TCPExecutor
        :returns: tcp executor
        """
        config = get_config(request)
        redis_noopexecutor = NoopRedis(
            host=host or config['host'],
            port=port or config['port'] or 6379,
            unixsocket=None
        )

        return redis_noopexecutor

    return redis_nooproc_fixture


def redisdb(process_fixture_name, dbnum=0, strict=True, decode=None):
    """
    Create connection fixture factory for pytest-redis.

    :param str process_fixture_name: name of the process fixture
    :param int dbnum: number of database to use
    :param bool strict: if true, uses StrictRedis client class
    :param bool decode_responses: Client: to decode response or not.
        See redis.StrictRedis decode_reponse client parameter.
    :rtype: func
    :returns: function which makes a connection to redis
    """
    @pytest.fixture
    def redisdb_factory(request):
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
        proc_fixture = request.getfixturevalue(process_fixture_name)
        config = get_config(request)

        redis_host = proc_fixture.host
        redis_port = proc_fixture.port
        redis_db = dbnum
        redis_class = redis.StrictRedis if strict else redis.Redis
        decode_responses = decode if decode is not None else config['decode']

        redis_client = redis_class(
            redis_host,
            redis_port,
            redis_db,
            unix_socket_path=proc_fixture.unixsocket,
            decode_responses=decode_responses
        )
        request.addfinalizer(redis_client.flushall)

        return redis_client

    return redisdb_factory


__all__ = ('redisdb', 'redis_proc')
