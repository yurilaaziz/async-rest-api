from barberousse.modules.base import WrapperModule


class ModuleCatalog:
    def __init__(self):
        self.modules = {}

    def register_module(self, module, name):
        if name not in self.modules:
            self.modules[name] = module

    def register_function(self, func, name):
        module = WrapperModule(func)
        self.register_module(module, name)


module_catalog = ModuleCatalog()
