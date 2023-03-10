import logging
import sys
from enum import Enum, auto
from functools import lru_cache
from typing import Literal

from dysession.settings import get_config

from .handler.colorful_console import ColorfulConsoleLoggerHandler


class LoggingType(Enum):
    """Enum of python logger type."""

    PLAINTEXT_CONSOLE = auto()
    COLOR_CONSOLE = auto()
    FILE = auto()
    CONSOLE = auto()


@lru_cache
def is_tty() -> bool:
    """Hepler function with lru_cache"""
    return sys.stdout.isatty()


def get_logger(
    logger_name: str = "dysession",
    logger_type: Literal[None, LoggingType.CONSOLE, LoggingType.FILE] = None,
    level: int = logging.DEBUG,
) -> logging.Logger:
    """
    This function return a logging.Logger with handlers.
    Handlers could be `ColorfulConsoleLoggerHandler`, `StreamHandler`, `FileHandler`.

    ```
    logger = get_logger()
    logger.debug("This is a DEBUG log.")
    logger.info("This is a INFO log.")
    logger.warning("This is a WARNING log.")
    logger.critical("This is a CRITICAL log.")
    logger.fatal("This is a FATAL log.")
    ```
    """

    if logger_type is None:
        try:
            logger_type = LoggingType[get_config()["LOGGING"]["TYPE"]]
            if (
                logger_type == LoggingType.PLAINTEXT_CONSOLE
                or logger_type == LoggingType.COLOR_CONSOLE
            ):
                raise KeyError
        except KeyError:
            raise KeyError("logger_type only accept 'CONSOLE' and 'FILE'")

    logger = logging.getLogger(logger_name)
    format = logging.Formatter(
        "[%(asctime)-s] [%(levelname)-8s] %(name)s %(message)s ... ( %(filename)s:%(levelno)s )"
    )
    logger.setLevel(level)

    if not logger.handlers:
        if logger_type == LoggingType.CONSOLE:
            if is_tty():
                handler = ColorfulConsoleLoggerHandler()
            else:
                handler = logging.StreamHandler()
        elif logger_type == LoggingType.FILE:
            filepath = get_config()["LOGGING"].get("FILE_PATH", "session.log")
            handler = logging.FileHandler(filepath, "a", encoding="utf-8")

        handler.setFormatter(format)
        logger.addHandler(handler)
    else:
        logger.warning(
            f"Dysession logger had already initialized with logger({logger.handlers})"
        )

    return logger


__all__ = (
    LoggingType,
    get_logger,
)
