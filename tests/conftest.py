from unittest.mock import patch

import pytest


@pytest.fixture
def clean_env():
    """
    Ensure no environment variables or real .env files interfere.
    """
    with (
        patch.dict("os.environ", clear=True),
        patch("pydantic_settings.sources.providers.dotenv.DotEnvSettingsSource._read_env_files", return_value={}),
    ):
        yield
