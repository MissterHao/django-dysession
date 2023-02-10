import logging
import sys
from enum import Enum, auto
from functools import lru_cache
from typing import Literal

from .handler.colorful_console import ColorfulConsoleLoggerHandler


class LoggingType(Enum):

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
    logger_type: Literal[LoggingType.CONSOLE, LoggingType.FILE] = LoggingType.CONSOLE,
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
            handler = logging.FileHandler("session.log", "a", encoding="utf-8")

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
