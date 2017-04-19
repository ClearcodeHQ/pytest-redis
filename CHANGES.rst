CHANGELOG
=========

unreleased
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
