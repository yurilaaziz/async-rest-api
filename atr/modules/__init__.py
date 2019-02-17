from importlib import import_module
from tempfile import TemporaryDirectory


class ModuleLoader:
    def __init__(self, module, args,
                 state,
                 notification_handler):

        module_split = module.rsplit('.', 1)
        if len(module_split) == 1:
            module_package = "atr.modules" + "." + module
        else:
            module_package = module

        self.module = import_module(module_package).Module()
        self.module.args = args
        self.module.notify = notification_handler
        self.module.state = state

    def __call__(self):
        with TemporaryDirectory() as temp_dir:
            self.module.temp_dir = temp_dir
            self.module.state.running()
            self.module.main()
