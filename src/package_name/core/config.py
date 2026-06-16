import os
import tomllib
from pathlib import Path

import structlog
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = structlog.getLogger(__name__)

CONFIG_DIR = Path(__file__).resolve().parents[3] / ".config"
ENV_MODE: str = os.getenv("APP_ENV", "dev").lower()


class DatabaseSettings(BaseModel):
    """
    Configuration schema for database connections.
    """

    host: str = Field(default="localhost")
    port: int = Field(default=1111)


class HTTPSettings(BaseModel):
    """
    Configuration schema for HTTP client settings.
    """

    base_url: str = Field(default="https://api.default.com")


class Settings(BaseSettings):
    """
    Main settings class that handles Pydantic validation and environment loading.
    """

    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / f".env.{ENV_MODE}"), env_file_encoding="utf-8", extra="ignore"
    )

    # SECRETS
    api_key: SecretStr = Field(default=SecretStr("default_secret"))
    database_url: SecretStr = Field(default=SecretStr("sqlite:///./default.db"))

    # APP Settings
    app_name: str = Field(default="package_name")

    # Nested APP Settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    http: HTTPSettings = Field(default_factory=HTTPSettings)

    @classmethod
    def load(cls) -> "Settings":
        """
        Load configuration from TOML files and merge with environment variables.

        Returns:
            Settings: An initialized configuration instance.
        """

        config_path = CONFIG_DIR / f"config.{ENV_MODE}.toml"
        toml_data = {}

        if config_path.exists():
            try:
                with open(config_path, "rb") as f:
                    toml_data = tomllib.load(f)
            except (tomllib.TOMLDecodeError, PermissionError) as e:
                logger.warning("Failed to load TOML data, fallback to defaults", exc_info=e)
            except Exception as e:
                logger.warning("Unexpected error reading TOML, fallback to defaults", exc_info=e)
        else:
            logger.warning("Missing config file, fallback to defaults", path=config_path)

        try:
            return cls(**toml_data)
        except Exception as e:
            logger.warning("Failed to validate TOML data, fallback to defaults", error=str(e))
            return cls()
