import logging
from typing import Dict

from .ansi import ANSIColor

LOGLEVEL_TRANSFORM: Dict[int, str] = {
    logging.DEBUG: ANSIColor.DEBUG.value,
    logging.INFO: ANSIColor.OKCYAN.value,
    logging.WARNING: ANSIColor.WARNING.value,
    logging.ERROR: ANSIColor.FAIL.value,
    logging.CRITICAL: ANSIColor.FAIL.value,
    logging.FATAL: ANSIColor.FAIL.value,
}


class ColorfulConsoleLoggerHandler(logging.StreamHandler):
    """
    A handler class which allows the cursor to stay on
    one line for selected messages
    """

    def emit(self, record):
        try:
            record.levelname = (
                LOGLEVEL_TRANSFORM[record.levelno]
                + f"{record.levelname:>8}"
                + ANSIColor.ENDC.value
            )

            msg = self.format(record)
            self.stream.write(msg)
            self.stream.write(self.terminator)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
