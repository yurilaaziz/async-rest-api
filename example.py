import logging
from time import sleep

from barberousse.api import app
from barberousse.gateway import Gateway

logger = logging.getLogger("root")

logger.setLevel(logging.DEBUG)

gateway = Gateway()


@gateway.task("sleep_well")
def sleepwell(seconds, notify):
    notify("sleeping for {}".format(seconds))
    sleep(seconds)
    notify("woke up")
    return 0


if __name__ == "__main__":
    app.run(debug=True)
