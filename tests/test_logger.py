import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog

from src.package_name.core.logger import (
    add_environment_info,
    mask_sensitive_data,
    setup_logging,
)


def test_add_environment_info_uses_app_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "TEST")

    event = add_environment_info(None, "", {})

    assert event["_env"] == "test"


def test_add_environment_info_defaults_to_dev(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)

    event = add_environment_info(None, "", {})

    assert event["_env"] == "dev"


def test_mask_sensitive_data_masks_sensitive_values():
    event = {
        "username": "user",
        "password": "secret",  # pragma: allowlist secret
        "access_token": "token-value",
        "api_key": "key-value",  # pragma: allowlist secret
        "auth_header": "bearer-value",
        "message": "hello",
    }

    result = mask_sensitive_data(None, "", event)

    assert result == {
        "username": "user",
        "password": "********",
        "access_token": "********",
        "api_key": "********",
        "auth_header": "********",
        "message": "hello",
    }


def test_mask_sensitive_data_is_case_insensitive():
    event = {
        "Password": "secret",  # pragma: allowlist secret
        "API_TOKEN": "token-value",
        "client_SECRET": "secret-value",  # pragma: allowlist secret
    }

    result = mask_sensitive_data(None, "", event)

    assert all(value == "********" for value in result.values())


def test_setup_logging_configures_pretty_console_logging():
    setup_logging(pretty_print=True)

    root_logger = logging.getLogger()

    assert root_logger.level == logging.INFO
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], logging.StreamHandler)
    assert not isinstance(root_logger.handlers[0], logging.FileHandler)


def test_setup_logging_configures_json_console_logging():
    setup_logging(pretty_print=False)

    root_logger = logging.getLogger()

    assert root_logger.level == logging.INFO
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], logging.StreamHandler)
    assert not isinstance(root_logger.handlers[0], logging.FileHandler)


def test_setup_logging_creates_rotating_log_file(tmp_path: Path):
    setup_logging(
        write_to_disk=True,
        log_dir=tmp_path,
        pretty_print=False,
    )

    log_file = tmp_path / "logs.json"

    assert log_file.exists()
    assert log_file.is_file()

    root_logger = logging.getLogger()

    assert len(root_logger.handlers) == 2
    assert any(isinstance(handler, RotatingFileHandler) for handler in root_logger.handlers)
    assert any(
        isinstance(handler, logging.StreamHandler) and not isinstance(handler, RotatingFileHandler)
        for handler in root_logger.handlers
    )


def test_setup_logging_configures_structlog():
    setup_logging()

    logger = structlog.get_logger("test")

    assert logger is not None
