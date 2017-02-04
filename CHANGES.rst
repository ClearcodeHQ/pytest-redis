CHANGELOG
=========

unreleased
-------

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
