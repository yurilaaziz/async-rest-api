from time import sleep

from .base import BaseModule


class Module(BaseModule):
    def main(self):
        sleep(10)
        return 0, "Success"
