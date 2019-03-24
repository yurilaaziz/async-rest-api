import logging.config
import os

from config42 import ConfigManager

from barberousse.default_config import DEFAULT_CONFIG

env_config = ConfigManager(prefix="BARBEROUSSE")
logging.basicConfig(level=logging.DEBUG if env_config.get("debug") else logging.INFO)
LOGGER = logging.getLogger(__name__)
if env_config.get("configcache"):
    config = ConfigManager(path=env_config.get("configcache"), defaults=DEFAULT_CONFIG)
else:
    config = ConfigManager(defaults=DEFAULT_CONFIG)

config.set_many(env_config.as_dict())
for component in ["worker", "database", "gateway"]:
    config_file = config.get(component + ".config.file")
    config_etcd = config.get(component + ".config.etcd")

    if config_file:
        if config_file.startswith("/"):
            config_path = config_file
        else:
            cwd = os.getcwd()
            config_path = cwd + "/" + config_file
        config.set_many({component: ConfigManager(path=config_path.replace('//', '/')).as_dict()})
        LOGGER.info("Setting configuration from {} for {} : OK".format(config_file, component))

    if config_etcd:
        if not config_etcd.get("keyspace"):
            raise Exception("etcd Keyspace is mandatory")
        try:
            config.set_many({component: ConfigManager(**config_etcd).as_dict()})
            LOGGER.info(
                "Setting external configuration from {} for {} : OK".format(config_file, component))
        except Exception as exc:
            LOGGER.error(
                "Setting external configuration from ({}) for {} : NOT OK".format(
                    ",".join({key + "=" + value for key, value in config_etcd.item() or {}}),
                    component))

            LOGGER.exception(exc)
            raise exc
    LOGGER.info("Setting of the {} has been finished successfully".format(component))

config.set("worker.broker.broker_url", config.get("worker.broker.broker_url").format(
    protocol=config.get("worker.connection.protocol"),
    username=config.get("worker.connection.username"),
    password=config.get("worker.connection.password"),
    host=config.get("worker.connection.host"),
    port=config.get("worker.connection.port")))
config.commit()
