import os

BARBEROUSSE_STANDALONE = os.getenv("BARBEROUSSE_STANDALONE", 0)
BARBEROUSSE_DEBUG = os.getenv("BARBEROUSSE_DEBUG", 0)
BARBEROUSSE_WORKER_CONFIG_FILE = os.getenv("BARBEROUSSE_WORKER_CONFIG_FILE")

BARBEROUSSE_WORKER_CONFIG_ETCD = {key.replace("BARBEROUSSE_WORKER_ETCD_", "").lower(): value for key, value in
                                  os.environ.items() if key.startswith("BARBEROUSSE_WORKER_ETCD_")}

BARBEROUSSE_PERSITENCE_CONFIG_FILE = os.getenv("BARBEROUSSE_PERSITENCE_CONFIG_FILE")
BARBEROUSSE_PERSITENCE_CONFIG_ETCD = {key.replace("BARBEROUSSE_PERSITENCE_CONFIG_", "").lower(): value for key, value in
                                      os.environ.items() if key.startswith("BARBEROUSSE_PERSITENCE_CONFIG_")}

BARBEROUSSE_GATEWAY_CONFIG_FILE = os.getenv("BARBEROUSSE_GATEWAY_CONFIG_FILE")
BARBEROUSSE_GATEWAY_CONFIG_ETCD = {key.replace("BARBEROUSSE_GATEWAY_CONFIG_", "").lower(): value for key, value in
                                   os.environ.items() if key.startswith("BARBEROUSSE_GATEWAY_CONFIG_")}
