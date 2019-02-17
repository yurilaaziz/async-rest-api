import pytest
from flask import Response as BaseResponse
from flask import json
from flask.testing import FlaskClient


class Response(BaseResponse):
    def open(self, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        kwargs.setdefault('data', {})
        kwargs['data'] = json.dumps(kwargs.get('data'))
        return super().open(*args, **kwargs)


class CustomClient(FlaskClient):
    def json(self):
        return json.loads(self.data.decode('utf-8'))


@pytest.fixture
def api_client():
    from atr.api import app
    app.test_client_class = CustomClient
    app.response_class = Response
    app.testing = True
    return app.test_client()
