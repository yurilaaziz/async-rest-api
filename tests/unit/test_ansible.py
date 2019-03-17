from bareberousse.utils.state import State


def test_git_clone_project(controller):
    uuid = controller.create_task(module="ansible",
                                  args=dict(
                                      src="git+https://github.com/yurilaaziz/async-rest-api",
                                      playbook="examples/ansible/site.yml"
                                  ))
    task = controller.get_task(uuid)
    assert task.get("status") == str(State.Success())


def test_local_copy_project(controller, cwd):
    uuid = controller.create_task(module="ansible",
                                  args=dict(
                                      src=cwd + "/examples/ansible",
                                      playbook="site.yml"
                                  ))
    task = controller.get_task(uuid)
    assert task.get("status") == str(State.Success())
