from atr.utils.state import Success
from .fixtures import api_client

__all__ = ['api_client']


def test_run_module(api_client):
    payload = dict(module="ansible", args="")

    resp = api_client.post('tasks', data=payload)
    assert resp.status_code == 201
    assert resp.json.get("uuid", None) is not None

    resp = api_client.get("task/" + resp.json["uuid"])

    assert resp.status_code == 200
    assert resp.json.get("status", None) is not None
    assert resp.json.get("status") == str(Success)


def test_failure_no_playbook(api_client):
    payload = dict(module="ansible",
                   args=dict(
                       playbook="no_playbook.yml"
                   ))

    resp = api_client.post('tasks', data=payload)
    assert resp.status_code == 201


def test_git_clone_project(api_client):
    payload = dict(module="ansible",
                   args=dict(
                       src="git+http://no_playbook.yml",
                       playbook="samples/ansible/no_playbook.yml"
                   ))
    resp = api_client.post('tasks', data=payload)
    assert resp.status_code == 201


def test_local_copy_project(api_client):
    payload = dict(module="ansible", args="")
    resp = api_client.post('tasks', data=payload)
    assert resp.status_code == 201
