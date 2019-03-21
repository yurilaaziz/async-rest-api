import logging.config
import os

from config42 import ConfigManager

from barberousse.default_config.constants import BARBEROUSSE_WORKER_CONFIG_FILE_DEFAULT, \
    BARBEROUSSE_PERSITENCE_CONFIG_FILE_DEFAULT, BARBEROUSSE_GATEWAY_CONFIG_FILE_DEFAULT
from barberousse.environement import BARBEROUSSE_WORKER_CONFIG_FILE, BARBEROUSSE_PERSITENCE_CONFIG_FILE, \
    BARBEROUSSE_WORKER_CONFIG_ETCD, BARBEROUSSE_PERSITENCE_CONFIG_ETCD, BARBEROUSSE_GATEWAY_CONFIG_FILE, \
    BARBEROUSSE_GATEWAY_CONFIG_ETCD, BARBEROUSSE_DEBUG

logging.basicConfig(level=logging.DEBUG if BARBEROUSSE_DEBUG else logging.INFO)

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

LOGGER = logging.getLogger(__name__)

config = {}
for component in components:
    _config = ConfigManager(path=component.get("default")).as_dict()
    LOGGER.info("Setting default configuration for {} : OK".format(component["name"]))
    if component.get("file"):
        if component["file"].startswith("/"):
            config_path = component["file"]
        else:
            cwd = os.getcwd()
            config_path = cwd + "/" + component["file"]
            _config.update(ConfigManager(path=config_path.replace('//', '/')).as_dict())
        LOGGER.info("Setting local configuration from {} for {} : OK".format(component["file"], component["name"]))

    if component["etcd"]:
        if not component["etcd"].get("keyspace"):
            raise Exception("etcd Keyspace is mandatory")
        try:
            _config.update(ConfigManager(**component["etcd"]).as_dict())
            LOGGER.info(
                "Setting external configuration from {} for {} : OK".format(component["file"], component["name"]))
        except Exception as exc:
            LOGGER.error(
                "Setting external configuration from ({}) for {} : NOT OK".format(
                    ",".join({key + "=" + value for key, value in component["etcd"].item() or {}}),
                    component["name"]))

            LOGGER.exception(exc)
            raise exc
    config.update({component["name"]: _config})
    LOGGER.info("Setting of the {} has been finished successfully".format(component["name"]))

config_worker = config["worker"]
config_db = config["database"]
config_gateway = config["gateway"]

_connection = config_worker["broker"].pop("connection")
config_worker["broker"]["broker_url"] = _connection["broker_url"].format(**_connection)
