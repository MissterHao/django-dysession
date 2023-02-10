import logging
import sys
from unittest import mock

from django.test import TestCase
from parameterized import parameterized

from dysession.logger import LoggingType, get_logger, is_tty
from dysession.logger.handler.colorful_console import ColorfulConsoleLoggerHandler


class LoggerTestCase(TestCase):
    def test_get_logger_with_second_logger_type_passed_in(self):

        with self.assertLogs("test_get_logger_with_second_logger_type_passed_in") as cm:
            logger = get_logger("test_get_logger_with_second_logger_type_passed_in")
            logger.info("This is a test content")
        self.assertIn("This is a test content", "\n".join(cm.output))

        with self.assertLogs("test_get_logger_with_second_logger_type_passed_in") as cm:
            logger = get_logger("test_get_logger_with_second_logger_type_passed_in", logger_type=LoggingType.FILE)
            logger.info("This is a test content")
        self.assertIn("WARNING", "\n".join(cm.output))

    @mock.patch("sys.stdout.isatty")
    def test_logger_is_tty_handlers(self, mock_is_tty):
        is_tty.cache_clear()
        mock_is_tty.return_value = True

        logger = get_logger("test_logger_is_tty_handlers")
        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.name, "test_logger_is_tty_handlers")
        self.assertIs(type(logger.handlers[0]), ColorfulConsoleLoggerHandler)

        logger.handlers = []

    @mock.patch("sys.stdout.isatty")
    def test_logger_is_not_tty_handlers(self, mock_is_tty):
        is_tty.cache_clear()
        mock_is_tty.return_value = False

        logger = get_logger("test_logger_is_not_tty_handlers")
        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.name, "test_logger_is_not_tty_handlers")
        self.assertIs(type(logger.handlers[0]), logging.StreamHandler)

        logger.handlers = []

    def test_logger_file_handler(self):

        logger = get_logger("test_logger_file_handler", logger_type=LoggingType.FILE)

        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.name, "test_logger_file_handler")
        self.assertIsInstance(logger.handlers[0], logging.FileHandler)

        with self.assertLogs("test_logger_file_handler") as cm:
            logger.info("This is a test content")
        self.assertIn("This is a test content", "\n".join(cm.output))

        logger.handlers = []
