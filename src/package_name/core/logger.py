import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import structlog

EventDict = dict[str, Any]
ProcessorType = Any


def setup_logging(
    write_to_disk: bool = False, log_dir: Path | None = None, pretty_print: bool = True, level: int = logging.INFO
) -> None:
    """
    Configure structlog and standard logging for the application.

    Parameters:
        write_to_disk (bool): Whether to save logs to a physical file.
        log_dir (Path | None): Directory where log files will be stored.
        pretty_print (bool): Use colorized console output instead of JSON.
        level (int): The logging level (e.g., logging.INFO).
    """

    custom_processors: list[ProcessorType] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        add_environment_info,
        structlog.stdlib.ExtraAdder(),
        mask_sensitive_data,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=custom_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    handlers: list[logging.Handler] = []

    if write_to_disk:
        log_dir = log_dir or Path(".log")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "logs.json"

        file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3)
        file_formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=custom_processors,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    if pretty_print:
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=custom_processors,
            processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, structlog.dev.ConsoleRenderer()],
        )
        console_handler.setFormatter(console_formatter)
        handlers.append(console_handler)
    else:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=custom_processors,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
        )
        stream_handler.setFormatter(stream_formatter)
        handlers.append(stream_handler)

    logging.basicConfig(level=level, handlers=handlers, force=True)


def add_environment_info(_: Any, __: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Inject the current environment name into the log event.

    Parameters:
        _: The logger instance (unused).
        __: The method name (unused).
        event_dict (dict): The current log event dictionary.

    Returns:
        dict: Updated dictionary with '_env' key.
    """

    event_dict["_env"] = os.getenv("APP_ENV", "dev").lower()
    return event_dict


def mask_sensitive_data(_: Any, __: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Scan log event keys for sensitive keywords and mask their values.

    Parameters:
        _: The logger instance (unused).
        __: The method name (unused).
        event_dict (dict): The current log event dictionary.

    Returns:
        dict: Updated dictionary with sensitive values replaced by asterisks.
    """
    sensitive_keywords = {"password", "token", "secret", "key", "auth"}

    for key in list(event_dict.keys()):
        if any(keyword in key.lower() for keyword in sensitive_keywords):
            event_dict[key] = "********"
    return event_dict
