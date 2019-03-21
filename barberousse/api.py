import logging.config

from flask import Flask
from flask_restplus import Api

from barberousse.config import config_gateway as config

logging.basicConfig(level="INFO")
logging.config.dictConfig((config.get('logging')))
from .db import connect_db
from .resources.task import namespace

app = Flask(__name__)
api = Api(app)
api.add_namespace(namespace)

connect_db()
