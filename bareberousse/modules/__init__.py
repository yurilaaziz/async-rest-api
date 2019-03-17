from importlib import import_module
from tempfile import TemporaryDirectory

from cerberus import Validator

from bareberousse.exceptions.module import TaskArgsValidationError


class ModuleLoader:
    def __init__(self, module, args,
                 state,
                 notification_handler):

        if "." not in module:
            module_package = "bareberousse.modules" + "." + module
        else:
            module_package = module

        self.module = import_module(module_package).Module()
        self.module.args = args
        self.module.notify = notification_handler
        self.module.state = state
        v = Validator(self.module.schema)
        if not v.validate(args):
            raise TaskArgsValidationError(str([e.schema_path for e in v._errors]))

    def __call__(self):
        with TemporaryDirectory() as temp_dir:
            self.module.temp_dir = temp_dir
            self.module.state.running()
            self.module.main()
