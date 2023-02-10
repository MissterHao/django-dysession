import logging
import sys
from enum import Enum, auto
from functools import lru_cache
from typing import Optional

from handler.colorful_console import ColorfulConsoleLoggerHandler


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
    logger_type: LoggingType = LoggingType.CONSOLE,
    level: int = logging.DEBUG,
) -> logging.Logger:

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

    return logger


if __name__ == "__main__":
    logger = get_logger()
    logger.debug("This is a DEBUG log.")
    logger.info("This is a INFO log.")
    logger.warning("This is a WARNING log.")
    logger.critical("This is a CRITICAL log.")
    logger.fatal("This is a FATAL log.")
