"""
Entry point for the project.

This is a placeholder implementation that initializes logging, configuration and
prints a basic startup message. Replace or extend `main()` with the
actual application logic as the project evolves.
"""

from pathlib import Path

import structlog

from package_name.utils.config import Settings
from package_name.utils.logger import setup_logging

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def main() -> None:
    """
    Main entry point of the application.

    Performs minimal setup:
      - Initializes logging
      - Loads configuration
      - Logs a simple startup message
    """

    # Initialize logging first so configuration loading is tracked
    setup_logging(write_to_disk=False, log_dir=Path("../../.log"))

    # Load settings
    settings = Settings.load()

    logger.info("Application started.", host=settings.database.host, api_key=settings.api_key)
    logger.info("Reached end of application.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical("Uncaught exception during startup", error=str(e))
        raise
