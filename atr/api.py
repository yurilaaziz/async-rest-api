from flask import Flask
from flask_restplus import Api

from .db import connect_db
from .resources.task import namespace

app = Flask(__name__)
api = Api(app)
api.add_namespace(namespace)

connect_db()

