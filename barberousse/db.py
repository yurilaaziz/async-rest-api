from mongoengine import connect

from .config import config_db as config


def connect_db():
    connect(**config)
