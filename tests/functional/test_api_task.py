from time import sleep

from barberousse.api_const import TASK_CREATED, TASK_FOUND
from barberousse.utils.state import State


def test_run_module(api_client):
    resp = api_client.post('tasks',
                           data=dict(module="delay",
                                     args=""))
    assert resp.status_code == TASK_CREATED
    assert resp.json.get("id", None) is not None
    uuid = resp.json["id"]
    for retry in range(5):

        resp = api_client.get("task/" + uuid)
        assert resp.status_code == TASK_FOUND
        assert (resp.json.get("status") == str(State.Success()) or resp.json.get("status") == str(State.Pending()))

        if resp.json.get("status") == str(State.Success()):
            break
        elif resp.json.get("status") == str(State.Pending()):
            sleep(1)

    else:
        Exception("Pending state persist")
