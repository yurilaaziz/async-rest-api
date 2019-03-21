import json
import logging

from mongoengine import DoesNotExist

from barberousse.environement import BARBEROUSSE_STANDALONE
from barberousse.persistences.task import Task as TaskModel
from barberousse.worker import task_executor


class Controller:
    def __init__(self, async_mode=None, **kwargs):
        self.logger = logging.getLogger(__name__)
        if not async_mode:
            self.async_mode = BARBEROUSSE_STANDALONE == 0

        self.logger.info("Initializing controller in {} mode".format(
            "Standalone" if not self.async_mode else "Distributed"
        ))

        self.async_mode = async_mode
        self.options = kwargs

    def create_task(self, module, args):
        self.logger.debug("Trying to create {} with {} args".format(module, len(args)))
        try:
            uuid = task_executor.init(module, args, self.options)
            self.logger.debug("Module {} has been initialized".format(module, len(args)))
        except Exception as exc:
            self.logger.error("Module {} failed while initializing ".format(module))
            self.logger.exception(exc)
            raise exc

        if not self.async_mode:
            _ = task_executor.run(uuid)
            self.logger.info("Module {} starts in synchronous mode".format(module))
        else:
            _ = task_executor.delay(uuid)
            self.logger.info("Module {} starts in Asynchronous mode".format(module))

        return uuid

    def get_task(self, uuid):
        try:
            task = TaskModel.objects.get(_id=uuid)
            task = json.loads(task.to_json())
        except DoesNotExist:
            task = None
        return task

    def get_tasks(self):
        tasks = TaskModel.objects()
        return json.loads(tasks.to_json())
