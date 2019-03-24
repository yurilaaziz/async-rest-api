LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "barberousse": {
            "level": "DEBUG",
            "handlers": [
                "console"
            ],
            "propagate": "no"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
}

DEFAULT_CONFIG = {
    "standalone": 0,
    "debug": 0,
    "worker": {
        "logging": LOGGING_CONFIG,

        "connection": {
            "username": "barberousse",
            "password": "barberousse",
            "host": "127.0.0.1",
            "port": 5672,
            "protocol": "amqp"
        },
        "broker": {
            "ignore_result": False,
            "result_backend": "amqp",
            "task_routes": {
                "barberousse.executor.Executor": {
                    "queue": "tasks"
                }
            }
        }
    },
    "database": {
        "logging": LOGGING_CONFIG,

        "connection": {
            "username": "barberousse",
            "password": "barberousse",
            "db": "admin",
            "host": "localhost",
            "port": 27017
        }

    },
    "gateway": {
        "logging": LOGGING_CONFIG,
    }
}
