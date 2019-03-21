import logging.config

from flask import Flask
from flask_restplus import Api

from barberousse.config import config_gateway as config
from .db import connect_db
from .resources.task import namespace

logging.config.dictConfig((config.get('logging')))

app = Flask(__name__)
api = Api(app)
api.add_namespace(namespace)

connect_db()
