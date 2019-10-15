# Copyright (C) 2017 by Clearcode <http://clearcode.cc>
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
"""Redis executor."""
import os
import re
from collections import namedtuple
from itertools import islice
from tempfile import gettempdir

from mirakuru import TCPExecutor


def compare_version(version1, version2):
    """
    Compare two version numbers.

    :param str version1: first version to compare
    :param str version2: second version to compare
    :rtype: int
    :returns: return value is negative if version1 < version2,
        zero if version1 == version2
        and strictly positive if version1 > version2
    """
    def normalize(ver):
        return [int(x) for x in re.sub(r'(\.0+)*$', '', ver).split(".")]

    def cmp_v(ver1, ver2):
        return (ver1 > ver2) - (ver1 < ver2)
    return cmp_v(normalize(version1), normalize(version2))


def extract_version(text):
    """
    Extract version number from the text.

    :param str text: text that contains the version number
    :rtype: str
    :returns: version number, e.g., "2.4.14"
    """
    match_object = re.search(r'\d+(?:\.\d+)+', text)
    if match_object:
        extracted_version = match_object.group(0)
    else:
        extracted_version = None
    return extracted_version


class RedisUnsupported(Exception):
    """Exception raised when redis<2.6 would be detected."""


class RedisMisconfigured(Exception):
    """Exception raised when the redis_exec points to non existing file."""


NoopRedis = namedtuple('NoopRedis', 'host, port, unixsocket')


class RedisExecutor(TCPExecutor):
    """
    Reddis executor.

    Extended TCPExecutor to contain all required logic for parametrising
    and properly constructing command to start redis-server.
    """

    MIN_SUPPORTED_VERSION = '2.6'
    """
    Minimum required version of redis that is accepted by pytest-redis.
    """

    def __init__(
            self, executable, databases, redis_timeout, loglevel, logsdir,
            host, port, timeout=60,
            logs_prefix='', save='', daemonize='no', rdbcompression=True,
            rdbchecksum=False, syslog_enabled=False,
            appendonly='no'
    ):  # pylint:disable=too-many-locals
        """
        Init method of a RedisExecutor.

        :param str executable: path to redis-server
        :param int databases: number of databases
        :param int redis_timeout: client's connection timeout
        :param str loglevel: redis log verbosity level
        :param str logdir: path to log directory
        :param str host: server's host
        :param int port: server's port
        :param int timeout: executor's timeout for start and stop actions
        :param str log_prefix: prefix for log filename
        :param str save: redis save configuration setting
        :param str daemonize:
        :param bool rdbcompression: Compress redis dump files
        :param bool rdbchecksum: Whether to add checksum to the rdb files
        :param bool syslog_enabled: Whether to enable logging
            to the system logger
        :param str appendonly:
        """
        self.unixsocket = gettempdir() + '/redis.{port}.sock'.format(port=port)
        self.executable = executable

        logfile_path = os.path.join(
            logsdir, '{prefix}redis-server.{port}.log'.format(
                prefix=logs_prefix,
                port=port
            )
        )

        command = [
            self.executable,
            '--daemonize', daemonize,
            '--rdbcompression', self._redis_bool(rdbcompression),
            '--rdbchecksum', self._redis_bool(rdbchecksum),
            '--appendonly', appendonly,
            '--databases', str(databases),
            '--timeout', str(redis_timeout),
            '--pidfile', 'redis-server.{port}.pid'.format(port=port),
            '--unixsocket', self.unixsocket,
            '--dbfilename', 'dump.{port}.rdb'.format(port=port),
            '--logfile', logfile_path,
            '--loglevel', loglevel,
            '--syslog-enabled', self._redis_bool(syslog_enabled),
            '--port', str(port),
            '--dir', gettempdir()
        ]
        if save:
            save_parts = save.split()
            assert all((part.isdigit() for part in save_parts)), \
                "all save arguments should be numbers"
            assert len(save_parts) % 2 == 0, \
                "there should be even number of elements passed to save"
            for time, change in zip(
                    islice(save_parts, 0, None, 2),
                    islice(save_parts, 1, None, 2)):
                command.extend(['--save {0} {1}'.format(time, change)])

        super(RedisExecutor, self).__init__(
            command, host, port, timeout=timeout
        )

    @classmethod
    def _redis_bool(cls, value):
        """
        Convert the boolean value to redis's yes/no.

        :param bool value: boolean value to convert
        :returns: yes for True, no for False
        :rtype: str
        """
        return 'yes' if value and value != 'no' else 'no'

    def start(self):
        """Check supported version before starting."""
        self._check_version()
        return super(RedisExecutor, self).start()

    def _check_version(self):
        """Check redises version if it's compatible."""
        with os.popen(
                '{0} --version'.format(self.executable)
        ) as version_output:
            version_string = version_output.read()
        if not version_string:
            raise RedisMisconfigured(
                'Bad path to redis_exec is given:'
                ' {0} not exists or wrong program'.format(
                    self.executable
                )
            )

        redis_version = extract_version(version_string)
        cv_result = compare_version(redis_version, self.MIN_SUPPORTED_VERSION)
        if redis_version and cv_result < 0:
            raise RedisUnsupported(
                'Your version of Redis is not supported. '
                'Consider updating to Redis {0} at least. '
                'The currently installed version of Redis: {1}.'
                .format(self.MIN_SUPPORTED_VERSION, redis_version))
