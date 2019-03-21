import os
from logging import getLogger

from config42 import ConfigManager

from barberousse.default_config.constants import BARBEROUSSE_WORKER_CONFIG_FILE_DEFAULT, \
    BARBEROUSSE_PERSITENCE_CONFIG_FILE_DEFAULT, BARBEROUSSE_GATEWAY_CONFIG_FILE_DEFAULT
from barberousse.environement import BARBEROUSSE_WORKER_CONFIG_FILE, BARBEROUSSE_PERSITENCE_CONFIG_FILE, \
    BARBEROUSSE_WORKER_CONFIG_ETCD, BARBEROUSSE_PERSITENCE_CONFIG_ETCD, BARBEROUSSE_GATEWAY_CONFIG_FILE, \
    BARBEROUSSE_GATEWAY_CONFIG_ETCD

components = [
    {
        "name": "worker",
        "default": BARBEROUSSE_WORKER_CONFIG_FILE_DEFAULT,
        "file": BARBEROUSSE_WORKER_CONFIG_FILE,
        "etcd": BARBEROUSSE_WORKER_CONFIG_ETCD,

    },
    {
        "name": "database",
        "default": BARBEROUSSE_PERSITENCE_CONFIG_FILE_DEFAULT,
        "file": BARBEROUSSE_PERSITENCE_CONFIG_FILE,
        "etcd": BARBEROUSSE_PERSITENCE_CONFIG_ETCD,

    },
    {
        "name": "gateway",
        "default": BARBEROUSSE_GATEWAY_CONFIG_FILE_DEFAULT,
        "file": BARBEROUSSE_GATEWAY_CONFIG_FILE,
        "etcd": BARBEROUSSE_GATEWAY_CONFIG_ETCD,

    }
]

LOGGER = getLogger(__name__)

config = {}
for component in components:
    _config = ConfigManager(path=component.get("default")).as_dict()

    if component.get("file"):
        if component["file"].startswith("/"):
            config_path = component["file"]
        else:
            cwd = os.getcwd()
            config_path = cwd + "/" + component["file"]
            _config.update(ConfigManager(path=config_path.replace('//', '/')).as_dict())

    if component["etcd"]:
        if not component["etcd"].get("keyspace"):
            raise Exception("etcd Keyspace is mandatory")
        try:
            _config.update(ConfigManager(**component["etcd"]).as_dict())
        except Exception as exc:
            LOGGER.exception(exc)
            raise exc

    config.update({component["name"]: _config})

config_worker = config["worker"]
config_db = config["database"]
config_gateway = config["gateway"]

_connection = config["worker"].get("broker").pop("connection")
config_worker["broker_url"] = _connection["broker_url"].format(**_connection)
del _connection
