import json
import logging

import structlog

from src.package_name.utils.logger import setup_logging


def test_logging_masking_and_env(capsys):
    """Test that sensitive data is masked and env info is added."""

    setup_logging(pretty_print=False, level=logging.INFO)
    log = structlog.get_logger()

    log.info("test_event", password="secret_password", user="jdoe")  # pragma: allowlist secret

    out, _ = capsys.readouterr()
    data = json.loads(out)

    assert data["password"] == "********"
    assert data["user"] == "jdoe"
    assert data["_env"] == "dev"
    assert data["event"] == "test_event"


def test_foreign_logger_integration(capsys):
    """Test that standard logging library calls are also processed/masked."""

    setup_logging(pretty_print=False)
    std_log = logging.getLogger("external_lib")

    std_log.warning("external_leak", extra={"token": "12345"})

    out, _ = capsys.readouterr()
    data = json.loads(out)

    assert data["logger"] == "external_lib"
    assert data["token"] == "********"


def test_file_logging(tmp_path):
    """Test that log files are created when write_to_disk is True."""

    log_dir = tmp_path / ".log"
    setup_logging(write_to_disk=True, log_dir=log_dir)
    log = structlog.get_logger()

    log.info("file_test")

    log_file = log_dir / "logs.json"
    assert log_file.exists()

    content = log_file.read_text()
    assert "file_test" in content
