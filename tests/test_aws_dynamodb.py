import boto3
from django.test import TestCase
from moto import mock_dynamodb

from dysession.aws.dynamodb import create_dynamodb_table, destory_dynamodb_table


class AWSDynamoDBTestCase(TestCase):
    @mock_dynamodb
    def test_init_dynamodb_table(self):

        options = {
            "pk": "abc",
            "sk": "def",
            "table": "sessions",
        }

        client = boto3.client("dynamodb")
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
            "pk": "abc",
            "sk": "def",
            "table": "sessions",
        }

        client = boto3.client("dynamodb")
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
            "pk": "abc",
            "sk": "def",
            "table": "sessions",
        }

        client = boto3.client("dynamodb")
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
            "pk": "abc",
            "sk": "def",
            "table": "sessions",
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
