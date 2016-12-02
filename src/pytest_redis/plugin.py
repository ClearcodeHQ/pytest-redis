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
"""Plugin configuration module for pytest-redis."""
from tempfile import gettempdir

from pytest_redis import factories


_help_exec = "Redis server executable"
_help_host = 'Host at which Redis will accept connections'
_help_port = 'Port at which Redis will accept connections'
_help_logsdir = "Logs directory location"


def pytest_addoption(parser):
    """Define configuration options."""
    parser.addini(
        name='redis_exec',
        help=_help_exec,
        default='/usr/bin/redis-server'
    )
    parser.addini(
        name='redis_host',
        help=_help_host,
        default='127.0.0.1'
    )
    parser.addini(
        name='redis_port',
        help=_help_port,
        default=None,
    )
    parser.addini(
        name='redis_logsdir',
        help=_help_logsdir,
        default=gettempdir(),
    )

    parser.addoption(
        '--redis-exec',
        action='store',
        dest='redis_exec',
        help=_help_exec,
    )
    parser.addoption(
        '--redis-host',
        action='store',
        dest='redis_host',
        help=_help_host,
    )
    parser.addoption(
        '--redis-port',
        action='store',
        dest='redis_port',
        help=_help_port
    )
    parser.addoption(
        '--redis-logsdir',
        action='store',
        metavar='path',
        help=_help_logsdir,
        dest='redis_logsdir',
    )


redis_proc = factories.redis_proc()
redisdb = factories.redisdb('redis_proc')
