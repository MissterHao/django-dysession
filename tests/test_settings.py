from django.test import TestCase
from parameterized import parameterized

from dysession.settings import get_config


class DysessionInitTestCase(TestCase):
    @parameterized.expand(
        [
            ("DYNAMODB_TABLENAME",),
            ("PARTITION_KEY_NAME",),
            ("SORT_KEY_NAME",),
            ("TTL_ATTRIBUTE_NAME",),
            ("CACHE_PERIOD",),
            ("DYNAMODB_REGION",),
        ]
    )
    def test_get_config_must_return_value_settings(self, config_key_name):
        self.assertTrue(config_key_name in get_config().keys())
