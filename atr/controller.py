from atr.worker import task_executor


class Controller:
    def __init__(self, **kwargs):
        self.async_mode = kwargs.get("async_mode", False)

    def create_task(self, module, args):

        try:
            uuid = task_executor.init(module, args)
        except Exception as exc:
            raise exc

        if not self.async_mode:
            _ = task_executor.run(uuid)
        else:
            _ = task_executor.delay(uuid)

        return uuid
