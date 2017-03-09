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
from itertools import islice
from tempfile import gettempdir

from mirakuru import TCPExecutor


class RedisExecutor(TCPExecutor):
    """
    Reddis executor.

    Extended TCPExecutor to contain all required logic for parametrising
    and properly constructing command to start redis-server.
    """

    def __init__(
        self, executable, databases, redis_timeout, loglevel, logsdir,
        logs_prefix='', save='', daemonize='no', rdbcompression=True,
        rdbchecksum=False, syslog_enabled=False,
        appendonly='no',  *args, **kwargs
    ):
        """
        Init method of a RedisExecutor.

        :param str executable: path to redis-server
        :param int databases: number of databases
        :param int redis_timeout: client's connection timeout
        :param str loglevel: redis log verbosity level
        :param str logdir: path to log directory
        :param str log_prefix: prefix for log filename
        :param str save: redis save configuration setting
        :param str daemonize:
        :param bool rdbcompression: Compress redis dump files
        :param bool rdbchecksum: Whether to add checksum to the rdb files
        :param bool syslog_enabled: Whether to enable logging
            to the system logger
        :param str appendonly:
        """
        port = kwargs.get('port')
        pidfile = 'redis-server.{port}.pid'.format(port=port)
        unixsocket = 'redis.{port}.sock'.format(port=port)
        dbfilename = 'dump.{port}.rdb'.format(port=port)

        logfile_path = os.path.join(
            logsdir, '{prefix}redis-server.{port}.log'.format(
                prefix=logs_prefix,
                port=port
            )
        )

        command = [
            executable,
            '--daemonize', daemonize,
            '--rdbcompression', self._redis_bool(rdbcompression),
            '--rdbchecksum', self._redis_bool(rdbchecksum),
            '--appendonly', appendonly,
            '--databases', str(databases),
            '--timeout', str(redis_timeout),
            '--pidfile', pidfile,
            '--unixsocket', unixsocket,
            '--dbfilename', dbfilename,
            '--logfile', logfile_path,
            '--loglevel', loglevel,
            '--syslog-enabled', self._redis_bool(syslog_enabled),
            '--port', str(port),
            '--dir', gettempdir()
        ]
        if save:
            save_parts = save.split()
            assert all((p.isdigit() for p in save_parts)), \
                "all save arguments should be numbers"
            assert len(save_parts) % 2 == 0, \
                "there should be even number of elements passed to save"
            for time, change in zip(
                    islice(save_parts, 0, None, 2),
                    islice(save_parts, 1, None, 2)):
                command.extend(['--save', '{0} {1}'.format(time, change)])

        super(RedisExecutor, self).__init__(
            command, *args, shell=True, **kwargs
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
