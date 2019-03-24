from logging import getLogger

from mongoengine import connect

from .config import config_db as config

LOGGER = getLogger(__name__)


def connect_db():
    _connection = config.get("connection")
    LOGGER.debug("Connecting to persistence backend {username}@{host}:{port}/{db}".format(
        username=_connection.get('username'),
        host=_connection.get('host'),
        port=_connection.get('port'),
        db=_connection.get('db')
    ))
    connect(**_connection)
