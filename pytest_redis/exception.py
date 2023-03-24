"""Pytest-Redis exceptions."""


class RedisUnsupported(Exception):
    """Exception raised when redis<2.6 would be detected."""


class RedisMisconfigured(Exception):
    """Exception raised when the redis_exec points to non existing file."""


class UnixSocketTooLong(Exception):
    """Exception raised when unixsocket path is too long."""
