import os
from pathlib import Path

import structlog
from pydantic import BaseModel, Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource

logger = structlog.get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = PROJECT_ROOT / ".config"
ENV_MODE: str = os.getenv("APP_ENV", "dev").lower()


class DatabaseSettings(BaseModel):
    """
    Configuration schema for database connections.
    """

    host: str = Field(default="localhost")
    port: int = Field(default=5432, ge=1, le=65535)

    url: SecretStr = Field(default=SecretStr("sqlite:///./default.db"))


class APISettings(BaseModel):
    """
    Configuration schema for HTTP client settings.
    """

    base_url: str = Field(default="https://api.default.com")

    key: SecretStr = Field(default=SecretStr("default_secret"))


class Settings(BaseSettings):
    """
    Main settings class that handles Pydantic validation and environment loading.
    """

    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / f".env.{ENV_MODE}"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        toml_file=CONFIG_DIR / f"config.{ENV_MODE}.toml",
        extra="ignore",
        frozen=True,
    )

    # APP Settings
    app_name: str = Field(default="package_name")

    # Nested APP Settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    api: APISettings = Field(default_factory=APISettings)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )

    @classmethod
    def load(cls) -> "Settings":
        """
        Load configuration from TOML files and environment variables.

        Returns:
            Settings: Validated application settings.

        Raises:
            ValidationError: If configuration values are invalid.
        """

        try:
            return cls()

        except ValidationError:
            logger.exception("Invalid application configuration")
            raise
