from argparse import ArgumentTypeError

from django.test import TestCase
from parameterized import parameterized

from dysession.management.commands._arg_types import positive_int


class DysessionInitTestCase(TestCase):
    @parameterized.expand([(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)])
    def test_pass_positive_int_to_positive_int(self, value):

        value = positive_int(value)
        assert value == value

    @parameterized.expand([(0,), (-1,), (-2,), (-3,), (-4,)])
    def test_pass_non_positive_number_to_positive_int(self, value):

        with self.assertRaises(ArgumentTypeError):
            value = positive_int(value)

