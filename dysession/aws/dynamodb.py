from datetime import datetime
from typing import Any, Dict, Optional, Union

import boto3
from django.utils import timezone

from dysession.aws.error import DynamodbTableNotFound
from dysession.backends.error import SessionKeyDoesNotExist, SessionKeyDuplicated

from ..settings import get_config


def create_dynamodb_table(options: Dict[str, Union[str, int]], client=None) -> Dict:

    if client is None:
        client = boto3.client("dynamodb", region_name=get_config()["DYNAMODB_REGION"])

    response = client.create_table(
        AttributeDefinitions=[
            {"AttributeName": options["pk"], "AttributeType": "S"},
            # {"AttributeName": options["sk"], "AttributeType": "S"},
        ],
        TableName=options["table"],
        KeySchema=[
            {"AttributeName": options["pk"], "KeyType": "HASH"},
            # {"AttributeName": options["sk"], "KeyType": "RANGE"},
        ],
        BillingMode="PAY_PER_REQUEST",
        TableClass="STANDARD",
    )

    return response


def destory_dynamodb_table(options: Dict[str, Union[str, int]], client=None) -> Dict:

    if client is None:
        client = boto3.client("dynamodb", region_name=get_config()["DYNAMODB_REGION"])

    response = client.delete_table(TableName=options["table"])
    return response


def check_dynamodb_table_exists(table_name: Optional[str] = None, client=None) -> Dict:

    if client is None:
        client = boto3.client("dynamodb", region_name=get_config()["DYNAMODB_REGION"])

    if table_name is None:
        table_name = get_config()["DYNAMODB_TABLENAME"]

    response = client.list_tables()
    if table_name not in response["TableNames"]:
        raise DynamodbTableNotFound

    return response


def key_exists(session_key: str, table_name: Optional[str] = None, client=None) -> bool:

    if client is None:
        client = boto3.client("dynamodb", region_name=get_config()["DYNAMODB_REGION"])

    if table_name is None:
        table_name = get_config()["DYNAMODB_TABLENAME"]

    assert type(session_key) is str, "session_key should be string type"

    pk = get_config()["PARTITION_KEY_NAME"]

    response = client.get_item(
        TableName=table_name,
        Key={
            pk: {"S": session_key},
        },
        ProjectionExpression=f"{pk}",
    )

    if "Item" in response:
        return True

    return False


def get_item(session_key: str, table_name: Optional[str] = None, client=None) -> bool:

    if client is None:
        client = boto3.client("dynamodb", region_name=get_config()["DYNAMODB_REGION"])

    if table_name is None:
        table_name = get_config()["DYNAMODB_TABLENAME"]

    assert type(session_key) is str, "session_key should be string type"

    pk = get_config()["PARTITION_KEY_NAME"]


def insert_session_item(
    session_key: str, table_name: Optional[str] = None, client=None
) -> bool:
    """Insert a session key"""

    if client is None:
        client = boto3.client("dynamodb", region_name=get_config()["DYNAMODB_REGION"])

    if table_name is None:
        table_name = get_config()["DYNAMODB_TABLENAME"]

    assert type(session_key) is str, "session_key should be string type"
    pk = get_config()["PARTITION_KEY_NAME"]


class DynamoDB:
    def __init__(self, client) -> None:
        pass

    def get(
        self, session_key: Optional[str] = None, ttl: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Return session data if dynamodb partision key is matched with inputed session_key"""
        return
        # if not found then raise
        raise SessionKeyDoesNotExist
        # if key is expired
        raise SessionExpired

    def set(self, session_key: Optional[str] = None, session_data=None) -> None:
        return
        # Partision key duplicated
        raise SessionKeyDuplicated

    def exists(self, session_key: Optional[str] = None) -> bool:
        return False
        # if not found then raise
        raise SessionKeyDoesNotExist
