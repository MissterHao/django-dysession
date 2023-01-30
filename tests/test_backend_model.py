from typing import Any

import boto3
from django.test import TestCase
from parameterized import parameterized

from dysession.backends.model import SessionDataModel


class SessionDataModelTestCase(TestCase):
    def test_init_without_session_key(self):
        model = SessionDataModel()
        self.assertIsNone(model.session_key)

    def test_init_with_session_key(self):
        model = SessionDataModel("string")
        self.assertEqual(model.session_key, "string")

    @parameterized.expand(
        [
            [1],
            [1.0],
            [True],
        ]
    )
    def test_init_with_wrong_type_session_key(self, wrong_type_session_key: Any):
        with self.assertRaises(TypeError):
            model = SessionDataModel(wrong_type_session_key)

    def test_set_attribute(self):
        model = SessionDataModel()
        model["good_key"] = 0

    def test_set_attribute_session_key(self):
        model = SessionDataModel()

        with self.assertRaises(ValueError):
            model["session_key"] = 0

    def test_get_attribute(self):
        model = SessionDataModel()
        model["good_key"] = 0

        self.assertEqual(model["good_key"], 0)

        with self.assertRaises(AttributeError):
            model["not_exist_key"]

    def test_get_function(self):
        model = SessionDataModel()
        model["good_key"] = 0

        self.assertEqual(model.get("good_key"), 0)
        self.assertEqual(model.get("not_exist_key", 10), 10)

        with self.assertRaises(AttributeError):
            model.get("not_exist_key")

    def test_get_function_default_value(self):
        model = SessionDataModel()
        model["good_key"] = 0

        self.assertEqual(model.get("good_key", 1), 0)
        self.assertIsNone(model.get("not_exist_key", default=None))

    def test_del_attribute(self):
        model = SessionDataModel()
        model["good_key"] = 0

        self.assertEqual(model["good_key"], 0)

        del model["good_key"]

        with self.assertRaises(AttributeError):
            model["good_key"]

    def test_pop_function(self):
        model = SessionDataModel()
        model["good_key"] = 0

        self.assertEqual(model.get("good_key"), 0)
        self.assertEqual(model.pop("good_key"), 0)

        with self.assertRaises(AttributeError):
            model.pop("not_exist_key")

    def test_get_function_default_value(self):
        model = SessionDataModel()
        model["good_key"] = 0

        self.assertEqual(model.get("good_key"), 0)
        self.assertEqual(model.pop("good_key"), 0)

        self.assertEqual(model.pop("good_key", 1), 1)

    def test_is_empty(self):
        model = SessionDataModel()
        self.assertTrue(model.is_empty)

        model["good_key"] = 0
        self.assertFalse(model.is_empty)

        del model["good_key"]
        self.assertTrue(model.is_empty)

    def test_iter(self):
        model = SessionDataModel()

        model["a"] = 1
        model["b"] = 1
        model["c"] = 1
        model["d"] = 1

        self.assertEqual(set(model), set(["a", "b", "c", "d"]))
