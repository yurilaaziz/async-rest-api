def test_configuration_content():
    from barberousse.config import config
    assert config.get("worker") is not None
    assert config.get("worker.broker") is not None
    assert config.get("worker.logging") is not None
    assert config.get("worker.broker.broker_url") is not None
    assert config.get("database") is not None
    assert config.get("gateway") is not None
    assert config.get("gateway.logging") is not None
    assert config.get("absent_component") is None


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
    assert config.get("worker.broker.broker_url") is not None
    assert str(local_config["connection"]["port"]) in config.get("worker.broker.broker_url")
