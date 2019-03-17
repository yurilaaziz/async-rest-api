from time import sleep

from .base import BaseModule


class Module(BaseModule):
    def main(self):
        sleep(10)
        return 0, "Success"

    schema = {
        "time": {'type': 'integer', 'required': False},
    }

    def main(self):
        sleep(self.args.get("time", 1))
        self.state.success()
