import json

from mongoengine import DoesNotExist
from barberousse.persistences.task import Task as TaskModel
from barberousse.worker import task_executor


class Controller:
    def __init__(self, async_mode=True, **kwargs):
        self.async_mode = async_mode
        self.options = kwargs

    def create_task(self, module, args):

        try:
            uuid = task_executor.init(module, args, self.options)
        except Exception as exc:
            raise exc

        if not self.async_mode:
            _ = task_executor.run(uuid)
        else:
            _ = task_executor.delay(uuid)

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
