import logging
import sys
import traceback
from datetime import datetime

from celery import Celery
from celery.app.task import Task

from bareberousse.db import connect_db
from .modules import ModuleLoader
from .persistences.task import Task as TaskModel
from .utils.state import State, Initializing, Pending

LOGGER = logging.getLogger(__name__)

from uuid import uuid4


class Executor(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._module = None
        self._uuid = None
        self.persistence = None
        self.buffer_max = 5
        self.buffer_count = 0
        self._disable_recover = False
        self._raise_error = False

    def init(self, module, args, options=None):
        status = State(Pending)
        self.persistence = TaskModel(_id=uuid4().hex)
        self.persistence.module = module
        self.persistence.time_start = datetime.utcnow()
        self.persistence.args = args
        self.persistence.status = str(status)
        self.persistence.save()

        for key, value in (options or {}).items():
            setattr(self, key, value)
        return self.persistence._id

    def recover(self, uuid):
        self.persistence = TaskModel.objects.get(_id=uuid)
        self.state = State(self.persistence.status)
        self.state.switch(Initializing)
        self.persistence.state = str(self.state)
        self.persistence.save()
        self._module = ModuleLoader(module=self.persistence.module,
                                    args=self.persistence.args,
                                    state=self.state,

                                    notification_handler=self.notify)

    def notify(self, output=None, state=None, error=None, commit=None):
        if output:
            self.persistence.traceback.append(output)
            self.buffer_count += 1
        if state:
            self.persistence.status = str(self.state)
            self.buffer_count += 1
        if error:
            self.persistence.error = error
        if commit or (commit is None and self.buffer_count > self.buffer_max):
            self.persistence.time_finish = datetime.utcnow()
            self.persistence.time = \
                (self.persistence.time_finish - self.persistence.time_start).total_seconds()
            self.persistence.save()
            self.buffer_max = 0

    def run(self, uuid):
        try:
            self.recover(uuid)
        except Exception as exc:
            LOGGER.exception(exc)
            raise exc

        try:
            _ = self._module()
            if not self.state.is_final():
                self.state.success()
        except Exception as exc:
            self.state.error()

            LOGGER.exception(exc)
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.notify(error=traceback.format_exception(exc_type, exc_value, exc_tb))
            if self._raise_error:
                raise exc
        finally:
            self.notify(state=self.state, commit=True)


connect_db()

# celery ignore result false
# broker url amqp://
# celery result backend
# celery routes path to class queue tasks

celery = Celery()
celery.config_from_object("bareberousse.celery_config")
task_executor = celery.register_task(Executor())
