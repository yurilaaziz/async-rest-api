from logging import getLogger

from mongoengine import connect

from .config import config_db as config

LOGGER = getLogger(__name__)


def connect_db():
    LOGGER.debug("Connecting to persistence backend {username}@{host}:{port}/{db}".format(
        username=config.get('username'),
        host=config.get('host'),
        port=config.get('port'),
        db=config.get('db')
    ))
    connect(**config)
