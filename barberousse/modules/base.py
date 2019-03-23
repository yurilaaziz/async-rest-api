import inspect

from barberousse.utils.state import State


class BaseModule:

    def main(self):
        raise NotImplementedError()


class WrapperModule(BaseModule):

    def __init__(self, f):

        class Module:
            def __init__(cls):
                cls.function = f
                cls.notify = print
                # inspect.signature(self.function).parameters
                cls.schema = None

            def main(cls):
                if "notify" in inspect.signature(cls.function).parameters:
                    status = cls.function(**cls.args, notify=cls.notify)
                else:
                    status = cls.function(**cls.args)

                if status:
                    cls.state.switch(State.Success)
                else:
                    cls.state.switch(State.Failed)

        self.wrapper = Module

    def __call__(self):
        return self.wrapper()
