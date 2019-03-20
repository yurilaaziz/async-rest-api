from logging import getLogger

from mongoengine import connect

from .config import config_db as config

LOGGER = getLogger(__name__)


def connect_db():
    print("Connecting to {username}@{host}:{port}/{db}".format(
        username=config.get('username'),
        host=config.get('host'),
        port=config.get('port'),
        db=config.get('db')
    ))
    connect(**config)
