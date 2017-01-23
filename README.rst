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

.. image:: https://travis-ci.org/ClearcodeHQ/pytest-redis.svg?branch=v1.1.1
    :target: https://travis-ci.org/ClearcodeHQ/pytest-redis
    :alt: Tests

.. image:: https://coveralls.io/repos/ClearcodeHQ/pytest-redis/badge.png?branch=v1.1.1
    :target: https://coveralls.io/r/ClearcodeHQ/pytest-redis?branch=v1.1.1
    :alt: Coverage Status

.. image:: https://requires.io/github/ClearcodeHQ/pytest-redis/requirements.svg?tag=v1.1.1
     :target: https://requires.io/github/ClearcodeHQ/pytest-redis/requirements/?tag=v1.1.1
     :alt: Requirements Status

What is this?
=============

This is a pytest plugin, that enables you to test your code that relies on a running Redis database.
It allows you to specify additional fixtures for Redis process and client.

How to use
==========

Plugin contains two fixtures

* **redis** - it's a client fixture that has functional scope. After each test, it cleans Redis database for more reliable tests.
* **redis_proc** - session scoped fixture, that starts Redis instance at it's first use and stops at the end of the tests.

Simply include one of these fixtures into your tests fixture list.

You can also create additional redis client and process fixtures if you'd need to:


.. code-block:: python

    from pytest_redis import factories

    redis_my_proc = factories.redis_proc(port=None, logsdir='/tmp')
    redis_my = factories.redis('redis_my_proc')

.. note::

    Each RabbitMQ process fixture can be configured in a different way than the others through the fixture factory arguments.

Configuration
=============

You can define your settings in three ways, it's fixture factory argument, command line option and pytest.ini configuration option.
You can pick which you prefer, but remember that these settings are handled in the following order:

    * ``Fixture factory argument``
    * ``Command line option``
    * ``Configuration option in your pytest.ini file``

+---------------------------+--------------------------+---------------------+-------------------+-----------------------+
| Redis option              | Fixture factory argument | Command line option | pytest.ini option | Default               |
+===========================+==========================+=====================+===================+=======================+
| executable                | executable               | --redis-exec        | redis_exec        | /usr/bin/redis-server |
+---------------------------+--------------------------+---------------------+-------------------+-----------------------+
| host                      | host                     | --redis-host        | redis_host        | 127.0.0.1             |
+---------------------------+--------------------------+---------------------+-------------------+-----------------------+
| port                      | port                     | --redis-port        | redis_port        | random                |
+---------------------------+--------------------------+---------------------+-------------------+-----------------------+
| connection timeout        | timeout                  | --redis-timeout     | redis_timeout     | 30                    |
+---------------------------+--------------------------+---------------------+-------------------+-----------------------+
| number of databases       | db_count                 | --redis-db-count    | redis_db_count    | 8                     |
+---------------------------+--------------------------+---------------------+-------------------+-----------------------+
| Log directory location    | logsdir                  | --redis-logsdir     | redis_logsdir     | $TMPDIR               |
+---------------------------+--------------------------+---------------------+-------------------+-----------------------+
| Redis log verbosity level | loglevel                 | --redis-loglevel    | redis_loglevel    | notice                |
+---------------------------+--------------------------+---------------------+-------------------+-----------------------+

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

Package resources
-----------------

* Bug tracker: https://github.com/ClearcodeHQ/pytest-redis/issues

