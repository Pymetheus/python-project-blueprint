import tomllib
from unittest.mock import MagicMock, patch

from src.package_name.utils.config import Settings


def test_settings_load_from_toml(clean_env):
    """Test that settings correctly load and merge TOML data."""
    mock_toml_dict = {"app_name": "test-app", "database": {"port": 9999}}

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("builtins.open", MagicMock()),
        patch("tomllib.load", return_value=mock_toml_dict),
    ):
        settings = Settings.load()
        assert settings.app_name == "test-app"
        assert settings.database.port == 9999
        assert settings.database.host == "localhost"


def test_settings_invalid_toml_fallback(clean_env):
    """Test fallback to defaults if TOML is corrupted."""

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("builtins.open", MagicMock()),
        patch("tomllib.load", side_effect=tomllib.TOMLDecodeError("Bad TOML")),
    ):
        settings = Settings.load()
        assert settings.app_name == "package_name"


def test_settings_unexpected_toml_fallback(clean_env):
    """Test fallback to defaults if unexpected error occurs."""

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("builtins.open", MagicMock()),
        patch("tomllib.load", side_effect=Exception),
    ):
        settings = Settings.load()
        assert settings.app_name == "package_name"


def test_settings_default_fallback(clean_env):
    """Test that settings return defaults when no file exists."""
    with patch("pathlib.Path.exists", return_value=False):
        settings = Settings.load()
        assert settings.app_name == "package_name"


def test_settings_pydantic_validation_error_fallback(clean_env):
    """Test fallback to defaults if TOML data fails Pydantic validation."""

    invalid_data = {"database": {"port": ["not", "an", "int"]}}

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("builtins.open", MagicMock()),
        patch("tomllib.load", return_value=invalid_data),
    ):
        settings = Settings.load()

        assert settings.database.port == 1111
        assert settings.app_name == "package_name"
