import logging
import sys
import traceback
from datetime import datetime

from celery import Celery
from celery.app.task import Task

from .modules import ModuleLoader
from .persistences.task import Task as TaskModel
from .utils.state import State

LOGGER = logging.getLogger(__name__)


class Executor(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._module = None
        self._uuid = None
        self.persistence = None
        self.buffer_max = 5
        self.buffer_count = 0

    def init(self, task):
        self.state = State()
        self.state.initializing()
        self._module = ModuleLoader(module="ansible",
                                    args=task.get('args'),
                                    state=self.state,

                                    notification_handler=self.notify)

        self._uuid = task.get('uuid')
        self.persistence = TaskModel(_id=self._uuid)

        self.persistence.module = task.get('module')
        self.persistence.time_start = datetime.utcnow()
        self.persistence.status = str(self.state)
        self.persistence.save()
        return self._uuid

    def notify(self, output=None, state=None, error=None, commit=None):
        if output:
            self.persistence.traceback.append(output)
            self.buffer_count += 1
        if state:
            self.persistence.status = str(self.state)
            self.buffer_count += 1
        if error:
            import sys
            self.persistence.error = error
        if commit or (commit is None and self.buffer_count > self.buffer_max):
            self.persistence.time_finish = datetime.utcnow()
            self.persistence.time = \
                (self.persistence.time_finish - self.persistence.time_start).total_seconds()
            self.persistence.save()
            self.buffer_max = 0

    def run(self, task):
        self.init(task)
        try:
            _ = self._module()
        except Exception as exc:
            self.state.error()
            LOGGER.exception(exc)
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.notify(error=traceback.format_exception(exc_type, exc_value, exc_tb))
        finally:
            self.notify(state=self.state, commit=True)


# connect_db()

# celery ignore result false
# broker url amqp://
# celery result backend
# celery routes path to class queue tasks

celery = Celery()
celery.config_from_object("atr.celery_config")
task_executor = celery.register_task(Executor())
