from django.test import TestCase
from parameterized import parameterized

from dysession.apps import DjangoDysessionConfig


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
    def test_django_app_config_is_correct(self, config_key_name):
        self.assertEqual(DjangoDysessionConfig.name, "dysession")
        self.assertEqual(
            DjangoDysessionConfig.verbose_name, "Django DynamoDB Session Backend"
        )
