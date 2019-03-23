from time import sleep

from .base import WrapperModule


@WrapperModule
def Module(seconds, notify):
    notify("sleeping for {}".format(seconds))
    sleep(seconds)
    notify("woke up")
    return 0
