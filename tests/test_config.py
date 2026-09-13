import pytest
from pydantic import ValidationError

from src.package_name.core.config import Settings


def test_load_uses_the_active_environment_configuration():
    settings = Settings.load()

    assert settings.app_name == "[[REPO_NAME]]"
    assert settings.database.host == "db.develop.com"


def test_environment_overrides_toml_configuration(monkeypatch):
    monkeypatch.setenv("DATABASE__HOST", "override-host")

    settings = Settings.load()

    assert settings.database.host == "override-host"


def test_invalid_environment_configuration_is_rejected(monkeypatch):
    monkeypatch.setenv("DATABASE__PORT", "0")

    with pytest.raises(ValidationError):
        Settings.load()
