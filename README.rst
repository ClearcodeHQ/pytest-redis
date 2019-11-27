.. image:: https://raw.githubusercontent.com/ClearcodeHQ/pytest-redis/master/logo.png
    :width: 100px
    :height: 100px
    
pytest-redis
============

.. image:: https://img.shields.io/pypi/v/pytest-redis.svg
    :target: https://pypi.python.org/pypi/pytest-redis/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/wheel/pytest-redis.svg
    :target: https://pypi.python.org/pypi/pytest-redis/
    :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/pytest-redis.svg
    :target: https://pypi.python.org/pypi/pytest-redis/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/pytest-redis.svg
    :target: https://pypi.python.org/pypi/pytest-redis/
    :alt: License

Package status
--------------

.. image:: https://travis-ci.org/ClearcodeHQ/pytest-redis.svg?branch=v2.0.0
    :target: https://travis-ci.org/ClearcodeHQ/pytest-redis
    :alt: Tests

.. image:: https://coveralls.io/repos/ClearcodeHQ/pytest-redis/badge.svg?branch=v2.0.0
    :target: https://coveralls.io/r/ClearcodeHQ/pytest-redis?branch=v2.0.0
    :alt: Coverage Status

What is this?
=============

This is a pytest plugin, that enables you to test your code that relies on a running Redis database.
It allows you to specify additional fixtures for Redis process and client.

How to use
==========

Plugin contains three fixtures

* **redisdb** - it's a client fixture that has functional scope. After each test, it cleans Redis database for more reliable tests.
* **redis_proc** - session scoped fixture, that starts Redis instance at it's first use and stops at the end of the tests.
* **redis_nooproc** - a nooprocess fixture, that's connecting to already running redis

Simply include one of these fixtures into your tests fixture list.

You can also create additional redis client and process fixtures if you'd need to:


.. code-block:: python

    from pytest_redis import factories

    redis_my_proc = factories.redis_proc(port=None, logsdir='/tmp')
    redis_my = factories.redisdb('redis_my_proc')

.. note::

    Each Redis process fixture can be configured in a different way than the others through the fixture factory arguments.


Connecting to already existing redis database
---------------------------------------------

Some projects are using already running redis servers (ie on docker instances).
In order to connect to them, one would be using the ``redis_nooproc`` fixture.

.. code-block:: python

    redis_external = factories.redisdb('redis_nooproc')

By default the  ``redis_nooproc`` fixture would connect to Redis instance using **6379** port. Standard configuration options apply to it.

These are the configuration options that are working on all levels with the ``redis_nooproc`` fixture:

Configuration
=============

You can define your settings in three ways, it's fixture factory argument, command line option and pytest.ini configuration option.
You can pick which you prefer, but remember that these settings are handled in the following order:

    * ``Fixture factory argument``
    * ``Command line option``
    * ``Configuration option in your pytest.ini file``

.. list-table:: Configuration options
   :header-rows: 1

   * - Redis server option
     - Fixture factory argument
     - Command line option
     - pytest.ini option
     - Noop process fixture
     - Default
   * - executable
     - executable
     - --redis-exec
     - redis_exec
     - -
     - /usr/bin/redis-server
   * - host
     - host
     - --redis-host
     - redis_host
     - host
     - 127.0.0.1
   * - port
     - port
     - --redis-port
     - redis_port
     - port
     - random
   * - connection timeout
     - timeout
     - --redis-timeout
     - redis_timeout
     - -
     - 30
   * - number of databases
     - db_count
     - --redis-db-count
     - redis_db_count
     - -
     - 8
   * - Whether to enable logging to the system logger
     - syslog
     - --redis-syslog
     - redis_syslog
     - -
     - False
   * - Log directory location
     - logsdir
     - --redis-logsdir
     - redis_logsdir
     - -
     - $TMPDIR
   * - Redis log verbosity level
     - loglevel
     - --redis-loglevel
     - redis_loglevel
     - -
     - notice
   * - Compress dump files
     - compress
     - --redis-compress
     - redis_compress
     - -
     - True
   * - Add checksum to RDB files
     - checksum
     - --redis-rdbcompress
     - redis_rdbchecksum
     - -
     - False
   * - Save configuration
     - save
     - --redis-save
     - redis_save
     - -
     - ""

Example usage:

* pass it as an argument in your own fixture

    .. code-block:: python

        redis_proc = factories.redis_proc(port=8888)

* use ``--redis-port`` command line option when you run your tests

    .. code-block::

        py.test tests --redis-port=8888


* specify your port as ``redis_port`` in your ``pytest.ini`` file.

    To do so, put a line like the following under the ``[pytest]`` section of your ``pytest.ini``:

    .. code-block:: ini

        [pytest]
        redis_port = 8888

Options below are for configuring redis client fixture.

+---------------------+--------------------------+---------------------+-------------------+---------+
| Redis client option | Fixture factory argument | Command line option | pytest.ini option | Default |
+=====================+==========================+=====================+===================+=========+
| decode_response     | decode                   | --redis-decode      | redis_decode      | False   |
+---------------------+--------------------------+---------------------+-------------------+---------+

Package resources
-----------------

* Bug tracker: https://github.com/ClearcodeHQ/pytest-redis/issues

