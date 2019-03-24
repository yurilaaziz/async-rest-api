from logging import getLogger

from mongoengine import connect

from .config import config

LOGGER = getLogger(__name__)


def connect_db():
    LOGGER.debug("Connecting to persistence backend {username}@{host}:{port}/{db}".format(
        username=config.get("database.connection.username"),
        host=config.get("database.connection.host"),
        port=config.get("database.connection.port"),
        db=config.get("database.connection.db")
    ))
    connect(username=config.get("database.connection.username"),
            password=config.get("database.connection.password"),
            host=config.get("database.connection.host"),
            port=config.get("database.connection.port"),
            db=config.get("database.connection.db"))
