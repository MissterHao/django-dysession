import time
from datetime import datetime
from typing import Any

import boto3
from django.test import TestCase
from moto import mock_dynamodb
from parameterized import parameterized

from dysession.aws.dynamodb import (
    DynamoDB,
    check_dynamodb_table_exists,
    create_dynamodb_table,
    destory_dynamodb_table,
    get_item,
    insert_session_item,
    key_exists,
)
from dysession.aws.error import DynamodbItemNotFound, DynamodbTableNotFound
from dysession.backends.error import (
    SessionExpired,
    SessionKeyDoesNotExist,
    SessionKeyDuplicated,
)
from dysession.backends.model import SessionDataModel
from dysession.settings import get_config


class DynamoDBTestCase(TestCase):
    @mock_dynamodb
    def create_dynamodb_table(self):
        self.options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        self.client = client = boto3.client(
            "dynamodb", region_name=self.options["region"]
        )
        try:
            check_dynamodb_table_exists(table_name=self.options["table"], client=client)
        except DynamodbTableNotFound:
            create_dynamodb_table(
                options={
                    "pk": self.options["pk"],
                    "sk": self.options["sk"],
                    "table": self.options["table"],
                },
                client=client,
            )

    @parameterized.expand(
        [
            ["aaaaaaa"],
            ["bbbbbbb"],
        ]
    )
    @mock_dynamodb
    def test_get_datamodel_from_dynamodb_controller(self, session_key: str):

        self.create_dynamodb_table()
        model = SessionDataModel(session_key)
        model["a"] = 1
        model["b"] = {"z": "z", "x": 1}
        model["c"] = False
        model["d"] = [7, 8, 9]
        model["e"] = "qwerty"

        resp = insert_session_item(data=model)
        self.assertEqual(resp["ResponseMetadata"]["HTTPStatusCode"], 200)

        db = DynamoDB(self.client)
        model = db.get(session_key)
        self.assertIsInstance(model, SessionDataModel)
        self.assertEqual(model.a, 1)
        self.assertEqual(len(model.b), 2)
        self.assertIn("z", model.b)
        self.assertIn("x", model.b)
        self.assertEqual(model.b["z"], "z")
        self.assertEqual(model.b["x"], 1)
        self.assertEqual(model.c, False)
        self.assertListEqual(model.d, [7, 8, 9])
        self.assertEqual(model.e, "qwerty")

    @mock_dynamodb
    def test_get_datamodel_from_dynamodb_controller_with_missing_session_key(self):

        db = DynamoDB(self.client)
        with self.assertRaises(ValueError):
            model = db.get()

    @mock_dynamodb
    def test_get_nonexist_datamodel_from_dynamodb_controller(self):

        self.create_dynamodb_table()

        db = DynamoDB(self.client)
        with self.assertRaises(SessionKeyDoesNotExist):
            model = db.get("not_exist")

    @mock_dynamodb
    def test_get_expired_datamodel_from_dynamodb_controller(self):

        session_key = "test_get_expired_datamodel_from_dynamodb_controller"
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp())
        insert_session_item(data=model, table_name=self.options["table"])

        # Make sure the item expired
        time.sleep(2)

        db = DynamoDB(self.client)
        with self.assertRaises(SessionExpired):
            model = db.get(session_key=session_key)

    @mock_dynamodb
    def test_get_not_expired_datamodel_from_dynamodb_controller(self):

        session_key = "test_get_not_expired_datamodel_from_dynamodb_controller"
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50
        insert_session_item(data=model, table_name=self.options["table"])

        # Make sure the item expired
        time.sleep(2)

        db = DynamoDB(self.client)

        model = db.get(session_key=session_key)

    @mock_dynamodb
    def test_set_datamodel_via_dynamodb_controller(self):

        session_key = "test_set_datamodel_via_dynamodb_controller"
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50

        db = DynamoDB(self.client)
        db.set(model, get_config()["DYNAMODB_TABLENAME"])

        query_model = db.get(session_key=session_key)
        self.assertEqual(model.a, query_model.a)

    @mock_dynamodb
    def test_set_duplicated_datamodel_via_dynamodb_controller_ignore_duplicated(self):

        session_key = "test_set_duplicated_datamodel_via_dynamodb_controller"
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50

        db = DynamoDB(self.client)
        db.set(model, get_config()["DYNAMODB_TABLENAME"])
        query_model = db.get(session_key=session_key)
        self.assertEqual(model.a, query_model.a)

        db.set(model, get_config()["DYNAMODB_TABLENAME"], ignore_duplicated=True)

    @mock_dynamodb
    def test_set_duplicated_datamodel_via_dynamodb_controller(self):

        session_key = "test_set_duplicated_datamodel_via_dynamodb_controller"
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50

        db = DynamoDB(self.client)
        db.set(model, get_config()["DYNAMODB_TABLENAME"])
        query_model = db.get(session_key=session_key)
        self.assertEqual(model.a, query_model.a)

        with self.assertRaises(SessionKeyDuplicated):
            db.set(model, get_config()["DYNAMODB_TABLENAME"], ignore_duplicated=False)

    @mock_dynamodb
    def test_exist_check_via_dynamodb_controller(self):

        session_key = "test_set_duplicated_datamodel_via_dynamodb_controller"
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50

        db = DynamoDB(self.client)
        db.set(model, get_config()["DYNAMODB_TABLENAME"])
        query_model = db.get(session_key=session_key)
        self.assertEqual(model.a, query_model.a)

        self.assertTrue(db.exists(session_key))
        self.assertFalse(db.exists(session_key + "_not_exists"))

    @parameterized.expand(
        [
            [1],
            [1.03],
            [True],
            [(1, 2, 3)],
            [[1, 2, 3]],
        ]
    )
    @mock_dynamodb
    def test_exist_check_input_type_error_via_dynamodb_controller(
        self, error_input: Any
    ):

        session_key = "test_set_duplicated_datamodel_via_dynamodb_controller"
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50

        db = DynamoDB(self.client)
        db.set(model, get_config()["DYNAMODB_TABLENAME"])
        query_model = db.get(session_key=session_key)
        self.assertEqual(model.a, query_model.a)

        with self.assertRaises(TypeError):
            db.exists(error_input)

    @mock_dynamodb
    def test_delete_item_via_dynamodb_controller(self):

        session_key = "test_set_duplicated_datamodel_via_dynamodb_controller"
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50

        db = DynamoDB(self.client)
        db.set(model, get_config()["DYNAMODB_TABLENAME"])
        query_model = db.get(session_key=session_key)
        self.assertEqual(model.a, query_model.a)

        db.delete(model)

    @mock_dynamodb
    def test_delete_item_via_dynamodb_controller_raise_error(self):

        session_key = None
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50
        model.session_key = 1

        db = DynamoDB(self.client)
        with self.assertRaises(AssertionError):
            db.delete(model)


    @mock_dynamodb
    def test_delete_item_via_dynamodb_controller_with_none_type_session_key(self):

        session_key = None
        self.create_dynamodb_table()

        model = SessionDataModel(session_key)
        model["a"] = 1
        model[get_config()["TTL_ATTRIBUTE_NAME"]] = int(datetime.now().timestamp()) + 50
        model.session_key = None

        db = DynamoDB(self.client)
        db.delete(model)