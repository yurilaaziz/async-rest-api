import logging
import sys
import traceback
from datetime import datetime
from uuid import uuid4

from celery.app.task import Task

from .loader import ModuleLoader
from .persistences.task import Task as TaskModel
from .utils.state import State, Initializing, Pending

LOGGER = logging.getLogger(__name__)
COMMIT_MSG = {False: "sent",
              True: "dalyed"}


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
        self.logger = logging.getLogger(__name__)

    def init(self, module, args, options=None):
        _ = ModuleLoader(module=module,
                         args=args,
                         state=None,
                         notification_handler=None)

        status = State(Pending)
        self.persistence = TaskModel(_id=uuid4().hex)
        self.persistence.module = module
        self.persistence.time_start = datetime.utcnow()
        self.persistence.args = args
        self.persistence.status = str(status)
        self.persistence.save()

        for key, value in (options or {}).items():
            setattr(self, key, value)

        self.logger.info("Persistence successful for task {}, module {} with {} args"
                         "".format(self.persistence._id, self.persistence.module,
                                   len(self.persistence.args)))
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
        self.logger.info("Recover successful for task {}, module {} with {} args"
                         "".format(self.persistence._id, self.persistence.module,
                                   len(self.persistence.args)))

    def notify(self, output=None, state=None, error=None, commit=None):
        to_commit = commit or (commit is None and self.buffer_count > self.buffer_max)

        if output:
            self.persistence.traceback.append(output)
            self.buffer_count += 1
            self.logger.debug("Notification {} : {} traceback updated with {} chars"
                              "".format(COMMIT_MSG[to_commit], self.persistence._id,
                                        len(output)))
        if state:
            self.persistence.status = str(self.state)
            self.buffer_count += 1
            self.logger.debug("Notification {} : {} state updated to {}"
                              "".format(COMMIT_MSG[to_commit], self.persistence._id, str(self.state)))

        if error:
            self.persistence.error = error
            self.logger.debug("Notification error {} : {}"
                              "".format(COMMIT_MSG[to_commit], self.persistence._id))
        if to_commit:
            self.persistence.time_finish = datetime.utcnow()
            self.persistence.time = \
                (self.persistence.time_finish - self.persistence.time_start).total_seconds()
            self.persistence.save()
            self.buffer_max = 0
            self.logger.debug("Notification buffer has been flushed for task {}"
                              "".format(self.persistence._id))

    def run(self, uuid):
        try:
            self.logger.info("Recovering task {}".format(uuid))
            self.recover(uuid)
        except Exception as exc:
            self.logger.error("Recovering failed for task {}".format(uuid))
            LOGGER.exception(exc)
            if self._raise_error:
                raise exc
            return

        try:
            _ = self._module()
            if not self.state.is_final():
                self.state.success()
        except Exception as exc:
            self.state.error()
            self.logger.error("Unhandled exception was thrown by task {}".format(uuid))
            self.logger.exception(exc)
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.notify(error=traceback.format_exception(exc_type, exc_value, exc_tb))
            if self._raise_error:
                raise exc
        finally:
            self.notify(state=self.state, commit=True)
