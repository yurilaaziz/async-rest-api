import logging.config

from celery import Celery

from barberousse.db import connect_db
from barberousse.executor import Executor
from .config import config_worker as config

try:
    logging.config.dictConfig(config.get('logging'))
except Exception as exc:
    logging.getLogger(__name__).error("Failed to set custom logging configuration")
    logging.getLogger(__name__).exception(exc)
connect_db()
celery = Celery()
celery.conf.update(**config.get('broker'))
task_executor = celery.register_task(Executor())
