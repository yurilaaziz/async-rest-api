from flask_restplus import Namespace, Resource, fields, reqparse, abort

from bareberousse.api_const import TASK_NOT_FOUND, TASK_CREATED, TASK_FOUND, TASK_ERROR

namespace = Namespace(name="task", path="/")
from bareberousse.controller import Controller

task_body = namespace.model("task", {
    'module': fields.String(description="Module name", required=True),
    'args': fields.Raw(description="Module", required=False)
})


@namespace.route('/tasks')
class Task(Resource):
    def get(self):
        controller = Controller()
        return controller.get_tasks()

    @namespace.doc(body=task_body)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("module", type=str, required=True)
        parser.add_argument("args", type=dict, required=False)
        args = parser.parse_args()
        controller = Controller()
        try:
            task_id = controller.create_task(args.get("module"), args.get("args"))
            task = {
                'module': args.get('module'),
                'id': task_id,
            }
            return task, TASK_CREATED
        except Exception as exc:
            task = {
                'module': args.get('module'),
                'message': str(exc),
            }
            return task, TASK_ERROR


@namespace.route('/task/<uuid>')
class Task(Resource):
    def get(self, uuid):
        controller = Controller()
        task = controller.get_task(uuid)
        if not task:
            abort(TASK_NOT_FOUND, "Task Not Found")
        else:
            return task, TASK_FOUND
