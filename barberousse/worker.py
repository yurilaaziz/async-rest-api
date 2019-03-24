import logging.config

from celery import Celery

from barberousse.db import connect_db
from barberousse.executor import Executor
from .config import config_worker as config

try:
    logging.config.dictConfig(config.get('logging'))
except:
    logging.getLogger(__name__).info("Failed to set custom logging configuration")
connect_db()
celery = Celery()
celery.conf.update(**config.get('broker'))
task_executor = celery.register_task(Executor())
