def test_configuration_content():
    from barberousse.config import config
    assert "worker" in config
    assert "broker" in config["worker"]
    assert "logging" in config["worker"]
    assert "broker_url" in config["worker"]["broker"]
    assert "database" in config
    assert "gateway" in config
    assert "logging" in config["gateway"]
    assert "absent_component" not in config


def test_set_configuration_file(cwd):
    import os
    config_path = cwd + "/tests/files/worker_task.json"
    os.environ["BARBEROUSSE_WORKER_CONFIG_FILE"] = config_path
    try:
        import sys
        del sys.modules['barberousse.config']
    except KeyError:
        pass
    from barberousse.config import config
    from config42 import ConfigManager
    local_config = ConfigManager(path=config_path).as_dict()
    assert "broker_url" in config["worker"]["broker"]
    assert str(local_config["connection"]["port"]) in config["worker"]["broker"]["broker_url"]
