from .fixtures import api_client

__all__ = ['api_client']


def test_create_task(api_client):
    resp = api_client.post('tasks', data=dict(module="ansible", args=""))
    assert resp.status_code == 200
