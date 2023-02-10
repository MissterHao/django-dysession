from typing import Any

from django.test import TestCase
from parameterized import parameterized

from dysession.logger import get_logger
from dysession.logger.handler.ansi import ANSIColor, colorful_it


class ANSITestCase(TestCase):
    @parameterized.expand(
        [
            [ANSIColor.HEADER],
            [ANSIColor.OKBLUE],
            [ANSIColor.OKCYAN],
            [ANSIColor.OKGREEN],
            [ANSIColor.SUCCESSFUL],
            [ANSIColor.WARNING],
            [ANSIColor.FAIL],
            [ANSIColor.DEBUG],
            [ANSIColor.BOLD],
            [ANSIColor.UNDERLINE],
        ]
    )
    def test_ansi_colorful_it_func(self, ansi_color: ANSIColor):

        self.assertEqual(
            colorful_it(ansi_color, "Content"),
            f"{ansi_color.value}Content{ANSIColor.ENDC.value}",
        )
