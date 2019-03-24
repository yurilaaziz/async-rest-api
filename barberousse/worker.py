import logging.config

from celery import Celery

from barberousse.db import connect_db
from barberousse.executor import Executor
from .config import config

try:
    logging.config.dictConfig(config.get("worker.logging"))
except Exception as exc:
    logging.getLogger(__name__).error("Failed to set custom logging configuration")
    logging.getLogger(__name__).exception(exc)
connect_db()
celery = Celery()

celery.conf.update(
    ignore_result=config.get("worker.broker.ignore_result"),
    result_backend=config.get("worker.broker.result_backend"),
    broker_url=config.get("worker.broker.broker_url"),
    task_routes=config.get("worker.broker.task_routes")
)
task_executor = celery.register_task(Executor())
