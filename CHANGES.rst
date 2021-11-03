CHANGELOG
=========

2.2.0
----------

Feature
-------

- Configure redis to listen on specific hostname exclusively using `--bind` parameter.

Misc
++++

- rely on `get_port` functionality delivered by `port_for`


2.1.1
----------

Misc
++++

- Rise more informative error when the unixsocket is too long. Now the error
  will hint at solution how to overcome it. This might be issue especially on
  MacOS, where the default temp folder is already a long path

2.1.0
----------

Features
++++++++

- Rely on tmpdir_factory for handling tmpdirs. Now it's cleanup should
  be handled better without much of the leftovers dangling indefinitely
  in the tmp directory.
- Store pidfile in fixture's temporary directory
- Support only python 3.7 and up

Backward incompatibilities
++++++++++++++++++++++++++

- Dropped `--redis-logsdir` command line option, `redis_logsdir` ini file
  configuration option and `logsdir` fixture factory configuration option.
  Logs will be automatically placed in fixture's temporary directory.
- Dropped `logs_prefix` argument from fixture factory argument

2.0.0
-------

- [feature] ability to properly connect to already existing postgresql server using ``redis_nooproc`` fixture.
- [enhancement] dropped support for python 2.7

1.3.2
-------

- [bugfix] - close file descriptor when reading redis version (by brunsgaard)

1.3.1
-------

- [bugfix] do not run redis explicitly with shell=True

1.3.0
-------

- [enhancement] RedisExecutor now provides attribute with path to unixsocket
- [enhancement] redis client fixture now connects to redis through unixsocket by default
- [enhancement] Version check got moved to executor, to be run just before starting Redis Server
- [feature] ability to configure decode_responses for redis client in command line, pytest.ini or factory argument.
- [bugfix] set decode_responses to False, same as StrictRedis default
- [enhancement] ability to change decode_responses value

1.2.1
-------

- [bugfix] raise specific error in case the redis executable path has been misconfigured or does not exists

1.2.0
-------

- [feature] ability to configure syslog-enabled for redis in command line, pytest.ini or factory argument.
- [feature] ability to configure rdbchecksum for redis in command line, pytest.ini or factory argument.
- [feature] ability to configure rdbcompression for redis in command line, pytest.ini or factory argument.
- [ehnacement] - RedisExecutor handling parameters and their translation to redis values if needed.
- [feature] ability to configure save option for redis in command line, pytest.ini or factory argument.

1.1.1
-------
- [cleanup] removed path.py dependency

1.1.0
-------

- [feature] - migrate usage of getfuncargvalue to getfixturevalue. require at least pytest 3.0.0

1.0.0
-------

- [enhancements] removed the possibility to pass the custom config. No need to include one in package now.
- [enhancements] command line, pytest.ini and fixture factory options for setting custom number of databases in redis
- [enhancements] command line, pytest.ini and fixture factory options for redis log verbosity
- [enhancements] command line, pytest.ini and fixture factory options for modifying connection timeout
- [enhancements] command line and pytest.ini options for modifying executable
- [enhancements] command line and pytest.ini options for modifying host
- [enhancements] command line and pytest.ini options for modifying port
- [enhancements] command line and pytest.ini options for modifying logs directory destination
