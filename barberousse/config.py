import os
from logging import getLogger

from config42 import ConfigManager

from barberousse.default_config.constants import BARBEROUSSE_WORKER_CONFIG_FILE_DEFAULT, \
    BARBEROUSSE_PERSITENCE_CONFIG_FILE_DEFAULT

LOGGER = getLogger(__name__)
BARBEROUSSE_WORKER_CONFIG_FILE = os.getenv("BARBEROUSSE_WORKER_CONFIG_FILE")

BARBEROUSSE_WORKER_ETCD = {key.replace("BARBEROUSSE_WORKER_ETCD_", "").lower(): value for key, value in
                           os.environ.items() if key.startswith("BARBEROUSSE_WORKER_ETCD_")}

BARBEROUSSE_PERSITENCE_CONFIG_FILE = os.getenv("BARBEROUSSE_PERSITENCE_CONFIG_FILE")

config_worker = ConfigManager(path=BARBEROUSSE_WORKER_CONFIG_FILE_DEFAULT).as_dict()

if BARBEROUSSE_WORKER_CONFIG_FILE:
    if BARBEROUSSE_WORKER_CONFIG_FILE.startswith("/"):
        config_path = BARBEROUSSE_WORKER_CONFIG_FILE
    else:
        cwd = os.getcwd()
        config_path = cwd + "/" + BARBEROUSSE_WORKER_CONFIG_FILE
    config_worker.update(ConfigManager(path=config_path.replace('//', '/')).as_dict())

if BARBEROUSSE_WORKER_ETCD:
    if not BARBEROUSSE_WORKER_ETCD.get("keyspace"):
        raise Exception("etcd Keyspace is mandatory")
    try:
        config_worker.update(ConfigManager(**BARBEROUSSE_WORKER_ETCD).as_dict())
    except Exception as exc:
        LOGGER.exception(exc)
        if not BARBEROUSSE_WORKER_CONFIG_FILE:
            raise exc

_broker = config_worker.pop("broker")
config_worker["broker_url"] = _broker["broker_url"].format(**_broker)
del _broker

config_db = ConfigManager(path=BARBEROUSSE_PERSITENCE_CONFIG_FILE_DEFAULT).as_dict()

if BARBEROUSSE_PERSITENCE_CONFIG_FILE:
    if BARBEROUSSE_PERSITENCE_CONFIG_FILE.startswith("/"):
        config_path = BARBEROUSSE_PERSITENCE_CONFIG_FILE
    else:
        cwd = os.getcwd()
        config_path = cwd + "/" + BARBEROUSSE_PERSITENCE_CONFIG_FILE
    config_db.update(ConfigManager(path=config_path.replace('//', '/')).as_dict())
