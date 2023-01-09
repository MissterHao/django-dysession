import boto3
from django.test import TestCase
from moto import mock_dynamodb

from dysession.aws.dynamodb import create_dynamodb_table, destory_dynamodb_table, check_dynamodb_table_exists
from dysession.aws.error import DynamodbTableNotFound


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
        response = check_dynamodb_table_exists(client=client)
    
    @mock_dynamodb
    def test_if_dynamodb_table_not_exist_with_client_input(self):

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

        
        with self.assertRaises(DynamodbTableNotFound):
            response = check_dynamodb_table_exists(table_name="notexist", client=client)

    @mock_dynamodb
    def test_if_dynamodb_table_not_exist(self):

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

        
        with self.assertRaises(DynamodbTableNotFound):
            response = check_dynamodb_table_exists(table_name="notexist")
    
    @mock_dynamodb
    def test_if_dynamodb_table_exist_then_no_exception_raised(self):

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

        
        check_dynamodb_table_exists(table_name=options["table"], client=client)    
