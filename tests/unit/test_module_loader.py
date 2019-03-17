from bareberousse.persistences.task import Task as TaskModel
from bareberousse.utils.state import State
from bareberousse.worker import task_executor

TEST_MODULE = "echo"


def test_initilizing():
    args = dict(message="hello")
    uuid = task_executor.init(TEST_MODULE, args)
    assert uuid is not None
    collection = TaskModel.objects.get(_id=uuid)
    assert collection.status == State.Pending.__name__
    assert collection.module == TEST_MODULE
    return uuid


def test_recover():
    uuid = test_initilizing()
    task_executor.recover(uuid)
    assert task_executor.state.is_equal(State.Initializing)
