from barberousse.catalog import module_catalog


class Gateway:
    def __init__(self):
        self.module_catalog = module_catalog

    def task(self, name):
        def wrapper(f):
            func_name = f.__name__ if not name else name
            self.module_catalog.register_function(f, func_name)

            return f

        return wrapper
