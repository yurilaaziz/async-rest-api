import json
from uuid import uuid4

from flask_restplus import Namespace, Resource, fields, reqparse, abort
from mongoengine import DoesNotExist

from ..persistences.task import Task as TaskModel
from ..utils.state import State
from ..worker import task_executor
from atr.api_const import TASK_NOT_FOUND , TASK_CREATED, TASK_FOUND
namespace = Namespace(name="task", path="/")

task_body = namespace.model("task", {
    'module': fields.String(description="Module name", required=True),
    'args': fields.Raw(description="Module", required=False)
})


@namespace.route('/tasks')
class Task(Resource):
    def get(self):
        tasks = TaskModel.objects()
        return json.loads(tasks.to_json())

    @namespace.doc(body=task_body)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("module", type=str, required=True)
        parser.add_argument("args", type=dict, required=False)
        args = parser.parse_args()
        uuid = uuid4().hex
        state = State()
        task = {
            'module': args.get('module'),
            'args': args.get('args', {}),
            'status': str(state),
            'uuid': uuid,
        }
        task_executor.init(task)
        try:
            result = task_executor.run(task)
        except Exception as exc:
            raise exc

        return task, TASK_CREATED


@namespace.route('/task/<uuid>')
class Task(Resource):
    def get(self, uuid):
        try:
            task = TaskModel.objects.get(_id=uuid)
        except DoesNotExist:
            abort(TASK_NOT_FOUND, "Task Not Found")
        return json.loads(task.to_json()), TASK_FOUND
