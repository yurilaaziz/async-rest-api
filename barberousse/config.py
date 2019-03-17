import os

from config42 import ConfigManager

from barberousse.default_config.constants import *

BARBEROUSSE_WORKER_CONFIG_FILE = os.getenv("BARBEROUSSE_WORKER_CONFIG_FILE")
BARBEROUSSE_WORKER_ETCD_HOST = os.getenv("BARBEROUSSE_WORKER_ETCD_HOST")
BARBEROUSSE_WORKER_ETCD_KEYSPACE = os.getenv("BARBEROUSSE_WORKER_ETCD_KEYSPACE")
BARBEROUSSE_WORKER_ETCD_USER = os.getenv("BARBEROUSSE_WORKER_ETCD_USER")
BARBEROUSSE_WORKER_ETCD_PASSWORD = os.getenv("BARBEROUSSE_WORKER_ETCD_PASSWORD")

BARBEROUSSE_PERSITENCE_CONFIG_FILE = os.getenv("BARBEROUSSE_PERSITENCE_CONFIG_FILE")

config_worker = ConfigManager(path=BARBEROUSSE_WORKER_CONFIG_FILE_DEFAULT).as_dict()

if BARBEROUSSE_WORKER_CONFIG_FILE:
    if BARBEROUSSE_WORKER_CONFIG_FILE.startswith("/"):
        config_path = BARBEROUSSE_WORKER_CONFIG_FILE
    else:
        cwd = os.getcwd()
        config_path = cwd + "/" + BARBEROUSSE_WORKER_CONFIG_FILE
    config_worker.update(ConfigManager(path=config_path.replace('//', '/')).as_dict())

config_worker["broker_url"] = config_worker["broker"]["broker_url"].format(
    **config_worker.get("broker"))

config_db = ConfigManager(path=BARBEROUSSE_PERSITENCE_CONFIG_FILE_DEFAULT).as_dict()
if BARBEROUSSE_PERSITENCE_CONFIG_FILE:
    if BARBEROUSSE_PERSITENCE_CONFIG_FILE.startswith("/"):
        config_path = BARBEROUSSE_PERSITENCE_CONFIG_FILE
    else:
        cwd = os.getcwd()
        config_path = cwd + "/" + BARBEROUSSE_PERSITENCE_CONFIG_FILE
    config_db.update(ConfigManager(path=config_path.replace('//', '/')).as_dict())
