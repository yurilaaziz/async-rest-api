import logging

from celery import Celery

from barberousse.db import connect_db
from barberousse.executor import Executor
from .config import config_worker as config

logging.basicConfig(**config.get('logging'))
connect_db()
celery = Celery()
celery.conf.update(**config.get('broker'))
task_executor = celery.register_task(Executor())
