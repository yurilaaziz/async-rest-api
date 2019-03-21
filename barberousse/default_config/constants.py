from os.path import dirname, realpath

BARBEROUSSE_DEFAULT_CONFIG_DIR = dirname(realpath(__file__))
BARBEROUSSE_WORKER_CONFIG_FILE_DEFAULT = BARBEROUSSE_DEFAULT_CONFIG_DIR + "/worker_task.json"
BARBEROUSSE_PERSITENCE_CONFIG_FILE_DEFAULT = BARBEROUSSE_DEFAULT_CONFIG_DIR + "/db.json"
BARBEROUSSE_GATEWAY_CONFIG_FILE_DEFAULT = BARBEROUSSE_DEFAULT_CONFIG_DIR + "/gateway.json"
