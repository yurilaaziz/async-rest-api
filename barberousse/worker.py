import logging

from celery import Celery

from barberousse.db import connect_db
from .config import config_worker as config

LOGGER = logging.getLogger(__name__)

from barberousse.executor import Executor

connect_db()
celery = Celery()
celery.conf.update(**config)
task_executor = celery.register_task(Executor())
