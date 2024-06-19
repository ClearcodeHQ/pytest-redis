"""Config loading helpers."""

from typing import Any, List, Optional, TypedDict

from _pytest.fixtures import FixtureRequest


class RedisConfigType(TypedDict):
    """Pytest redis config definition type."""

    host: str
    port: Optional[int]
    username: str
    password: str
    exec: str
    timeout: int
    loglevel: str
    db_count: int
    save: str
    compression: bool
    rdbchecksum: bool
    syslog: bool
    decode: bool
    datadir: str
    modules: List[str]


def get_config(request: FixtureRequest) -> RedisConfigType:
    """Return a dictionary with config options."""

    def get_conf_option(option: str) -> Any:
        option_name = "redis_" + option
        return request.config.getoption(option_name) or request.config.getini(option_name)

    port = get_conf_option("port")
    if modules := get_conf_option("modules"):
        modules = modules.split(",")
    else:
        modules = []
    config: RedisConfigType = {
        "host": get_conf_option("host"),
        "port": int(port) if port else None,
        "username": get_conf_option("username"),
        "password": get_conf_option("password"),
        "exec": get_conf_option("exec"),
        "timeout": int(get_conf_option("timeout")),
        "loglevel": get_conf_option("loglevel"),
        "db_count": int(get_conf_option("db_count")),
        "save": get_conf_option("save"),
        "compression": bool(get_conf_option("compression")),
        "rdbchecksum": bool(get_conf_option("rdbchecksum")),
        "syslog": bool(get_conf_option("syslog")),
        "decode": bool(get_conf_option("decode")),
        "datadir": get_conf_option("datadir"),
        "modules": modules,
    }
    return config
