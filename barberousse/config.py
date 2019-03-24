import logging.config
import os

from config42 import ConfigManager

from barberousse.default_config import DEFAULT_CONFIG

env_config = ConfigManager(prefix="BARBEROUSSE", defaults=DEFAULT_CONFIG)

logging.basicConfig(level=logging.DEBUG if env_config.get("debug") else logging.INFO)

LOGGER = logging.getLogger(__name__)

config = DEFAULT_CONFIG
for component in ["worker", "database", "gateway"]:
    config_file = env_config.get(component + ".config.file")
    config_etcd = env_config.get(component + ".config.etcd")

    _config = env_config.get(component)
    LOGGER.info("Setting configuration from Environment for {}, {} vars loaded: OK".format(component, len(_config)))
    if config_file:
        if config_file.startswith("/"):
            config_path = config_file
        else:
            cwd = os.getcwd()
            config_path = cwd + "/" + config_file
        _config.update(ConfigManager(path=config_path.replace('//', '/')).as_dict())
        LOGGER.info("Setting configuration from {} for {} : OK".format(config_file, component))

    if config_etcd:
        if not config_etcd.get("keyspace"):
            raise Exception("etcd Keyspace is mandatory")
        try:
            _config.update(ConfigManager(**config_etcd).as_dict())
            LOGGER.info(
                "Setting external configuration from {} for {} : OK".format(config_file, component))
        except Exception as exc:
            LOGGER.error(
                "Setting external configuration from ({}) for {} : NOT OK".format(
                    ",".join({key + "=" + value for key, value in config_etcd.item() or {}}),
                    component))

            LOGGER.exception(exc)
            raise exc
    config[component].update(_config)
    LOGGER.info("Setting of the {} has been finished successfully".format(component))

config_worker = config["worker"]
config_db = config["database"]
config_gateway = config["gateway"]
_connection = config_worker["connection"]

if not config_worker["connection"].get("broker_url"):
    config_worker["connection"]["broker_url"] = "{protocol}://{username}:{password}@{host}:{port}"
config_worker["broker"]["broker_url"] = config_worker["connection"]["broker_url"].format(**_connection)
