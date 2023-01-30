import boto3
from django.test import TestCase
from moto import mock_dynamodb
from parameterized import parameterized

from dysession.aws.dynamodb import (
    check_dynamodb_table_exists,
    create_dynamodb_table,
    destory_dynamodb_table,
    insert_session_item,
    key_exists,
)
from dysession.aws.error import DynamodbTableNotFound
from dysession.settings import get_config


class AWSDynamoDBTestCase(TestCase):
    @mock_dynamodb
    def test_init_dynamodb_table(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        response = create_dynamodb_table(
            options={
                "pk": options["pk"],
                "sk": options["sk"],
                "table": options["table"],
            },
            client=client,
        )

        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        self.assertEqual(response["TableDescription"]["TableName"], options["table"])

    @mock_dynamodb
    def test_init_dynamodb_table_with_client_input(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        response = create_dynamodb_table(
            options={
                "pk": options["pk"],
                "sk": options["sk"],
                "table": options["table"],
            },
        )

        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        self.assertEqual(response["TableDescription"]["TableName"], options["table"])

    @mock_dynamodb
    def test_destory_dynamodb_table(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        create_dynamodb_table(
            options={
                "pk": options["pk"],
                "sk": options["sk"],
                "table": options["table"],
            },
            client=client,
        )
        response = destory_dynamodb_table(options=options, client=client)

        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        self.assertEqual(response["TableDescription"]["TableName"], options["table"])

    @mock_dynamodb
    def test_destory_dynamodb_table_with_client_input(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        create_dynamodb_table(
            options={
                "pk": options["pk"],
                "sk": options["sk"],
                "table": options["table"],
            },
        )
        response = destory_dynamodb_table(options=options)

        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        self.assertEqual(response["TableDescription"]["TableName"], options["table"])

    @mock_dynamodb
    def test_destory_dynamodb_table(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        create_dynamodb_table(
            options={
                "pk": options["pk"],
                "sk": options["sk"],
                "table": options["table"],
            },
            client=client,
        )
        response = check_dynamodb_table_exists(client=client)

    @mock_dynamodb
    def test_if_dynamodb_table_not_exist_with_client_input(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        create_dynamodb_table(
            options={
                "pk": options["pk"],
                "sk": options["sk"],
                "table": options["table"],
            },
            client=client,
        )

        with self.assertRaises(DynamodbTableNotFound):
            response = check_dynamodb_table_exists(table_name="notexist", client=client)

    @mock_dynamodb
    def test_if_dynamodb_table_not_exist(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        create_dynamodb_table(
            options={
                "pk": options["pk"],
                "sk": options["sk"],
                "table": options["table"],
            },
        )

        with self.assertRaises(DynamodbTableNotFound):
            response = check_dynamodb_table_exists(table_name="notexist")

    @mock_dynamodb
    def test_if_dynamodb_table_exist_then_no_exception_raised(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        create_dynamodb_table(
            options={
                "pk": options["pk"],
                "sk": options["sk"],
                "table": options["table"],
            },
            client=client,
        )

        check_dynamodb_table_exists(table_name=options["table"], client=client)

    @mock_dynamodb
    def test_check_if_key_not_exist(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        try:
            check_dynamodb_table_exists(table_name=options["table"], client=client)
        except DynamodbTableNotFound:
            create_dynamodb_table(
                options={
                    "pk": options["pk"],
                    "sk": options["sk"],
                    "table": options["table"],
                },
                client=client,
            )

        key_exists(
            session_key="opiugyf",
            table_name=options["table"],
            client=client,
        )

    @mock_dynamodb
    def test_check_if_key_exist(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        try:
            check_dynamodb_table_exists(table_name=options["table"], client=client)
        except DynamodbTableNotFound:
            create_dynamodb_table(
                options={
                    "pk": options["pk"],
                    "sk": options["sk"],
                    "table": options["table"],
                },
                client=client,
            )
        key_exists(
            session_key="oijhugvfc",
            table_name=options["table"],
            client=client,
        )

    @mock_dynamodb
    def test_check_key_wrong_type(self):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        try:
            check_dynamodb_table_exists(table_name=options["table"], client=client)
        except DynamodbTableNotFound:
            create_dynamodb_table(
                options={
                    "pk": options["pk"],
                    "sk": options["sk"],
                    "table": options["table"],
                },
                client=client,
            )

        with self.assertRaises(AssertionError):
            key_exists(
                session_key=123,
                table_name=options["table"],
                client=client,
            )

    # Get Item
    @parameterized.expand(
        [
            ["aaaaaaaaa"],
            ["bbbbbbbbb"],
            ["ccccccccc"],
        ]
    )
    @mock_dynamodb
    def test_insert_item(self, session_key: str):

        options = {
            "pk": get_config()["PARTITION_KEY_NAME"],
            "sk": get_config()["SORT_KEY_NAME"],
            "table": "sessions",
            "region": "ap-northeast-1",
        }

        client = boto3.client("dynamodb", region_name=options["region"])
        try:
            check_dynamodb_table_exists(table_name=options["table"], client=client)
        except DynamodbTableNotFound:
            create_dynamodb_table(
                options={
                    "pk": options["pk"],
                    "sk": options["sk"],
                    "table": options["table"],
                },
                client=client,
            )

        insert_session_item(
            session_key=session_key,
            table_name=options["table"],
            client=client,
        )
