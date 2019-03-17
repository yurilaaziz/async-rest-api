from time import sleep

from .base import BaseModule


class Module(BaseModule):
    schema = {
        "time": {'type': 'integer', 'required': False},
    }

    def main(self):
        sleep(self.args.get("time", 1))
        self.state.success()
