import logging
from datetime import datetime
from typing import Any, Callable, Dict, Literal, Optional, Union

import boto3
from botocore import client as botoClitent
from django.utils import timezone

from dysession.aws.error import DynamodbItemNotFound, DynamodbTableNotFound
from dysession.backends.error import (
    SessionExpired,
    SessionKeyDoesNotExist,
    SessionKeyDuplicated,
)
from dysession.backends.model import SessionDataModel
from dysession.logger import get_logger

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
        raise DynamodbTableNotFound(table_name)

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
    return "Item" in response


def get_item(session_key: str, table_name: Optional[str] = None) -> SessionDataModel:

    if table_name is None:
        table_name = get_config()["DYNAMODB_TABLENAME"]

    assert type(session_key) is str, "session_key should be string type"

    logging.info("Get Item from DynamoDB")

    pk = get_config()["PARTITION_KEY_NAME"]

    resource = boto3.resource("dynamodb", region_name=get_config()["DYNAMODB_REGION"])
    table = resource.Table(table_name)

    response = table.get_item(
        Key={
            pk: session_key,
        },
    )

    if "Item" not in response:
        raise DynamodbItemNotFound()

    model = SessionDataModel(session_key=session_key)
    for k, v in response["Item"].items():
        model[k] = v
    return model


def insert_session_item(
    data: SessionDataModel,
    table_name: Optional[str] = None,
    return_consumed_capacity: Literal["INDEXES", "TOTAL", "NONE"] = "TOTAL",
    ignore_duplicated: bool = True,
) -> bool:
    """Insert a session key"""

    assert type(data.session_key) is str, "session_key should be string type"

    if table_name is None:
        table_name = get_config()["DYNAMODB_TABLENAME"]

    if not ignore_duplicated and key_exists(data.session_key):
        logger = get_logger()
        logger.error(f"'{data.session_key}' is already an item of table '{table_name}'.")
        raise SessionKeyDuplicated

    resource = boto3.resource("dynamodb", region_name=get_config()["DYNAMODB_REGION"])
    table = resource.Table(table_name)
    pk = get_config()["PARTITION_KEY_NAME"]

    insert_item = {pk: data.session_key}
    for key in data:
        insert_item[key] = data[key]

    response = table.put_item(
        TableName=table_name,
        Item=insert_item,
        ReturnConsumedCapacity=return_consumed_capacity,
    )

    return response


def delete_session_item(
    data: SessionDataModel,
    table_name: Optional[str] = None,
) -> bool:
    """Delete a session key"""

    assert type(data.session_key) is str, "session_key should be string type"

    if table_name is None:
        table_name = get_config()["DYNAMODB_TABLENAME"]

    resource = boto3.resource("dynamodb", region_name=get_config()["DYNAMODB_REGION"])
    table = resource.Table(table_name)
    pk = get_config()["PARTITION_KEY_NAME"]

    insert_item = {pk: data.session_key}
    for key in data:
        insert_item[key] = data[key]

    response = table.delete_item(
        Key={pk: data.session_key},
    )

    return response


class DynamoDB:
    def __init__(self, client=None) -> None:
        self.client = client

    def get(
        self,
        session_key: Optional[str] = None,
        table_name: Optional[str] = None,
        expired_time_fn: Callable[[], datetime] = datetime.now,
    ) -> Dict[str, Any]:
        """Return session data if dynamodb partision key is matched with inputed session_key"""
        if session_key is None:
            raise ValueError("session_key should be str type")

        if table_name is None:
            table_name = get_config()["DYNAMODB_TABLENAME"]

        now = expired_time_fn()

        try:
            model = get_item(session_key=session_key, table_name=table_name)
            if get_config()["TTL_ATTRIBUTE_NAME"] in model:
                time = model[get_config()["TTL_ATTRIBUTE_NAME"]]
                if time < int(now.timestamp()):
                    raise SessionExpired
        # if not found then raise
        except DynamodbItemNotFound:
            logger = get_logger()
            logger.error(f"'{session_key}' cannot be found on table '{table_name}'.")
            raise SessionKeyDoesNotExist
        # if key is expired
        except SessionExpired:
            logger = get_logger()
            logger.error(f"'{session_key}' is expired .")
            raise SessionExpired

        return model

    def set(
        self,
        data: SessionDataModel,
        table_name: Optional[str] = None,
        return_consumed_capacity: Literal["INDEXES", "TOTAL", "NONE"] = "TOTAL",
        ignore_duplicated: bool = True,
    ) -> None:
        try:
            insert_session_item(
                data,
                table_name,
                return_consumed_capacity,
                ignore_duplicated=ignore_duplicated,
            )
        except SessionKeyDuplicated:
            if not ignore_duplicated:
                raise SessionKeyDuplicated

    def exists(self, session_key: str) -> bool:
        if type(session_key) is not str:
            raise TypeError(
                f"session_key should be type of str instead of {type(session_key)}."
            )

        return key_exists(session_key=session_key)

    def delete(self, data: SessionDataModel, table_name: Optional[str] = None) -> bool:
        if data.session_key is None:
            return

        try:
            delete_session_item(data=data, table_name=table_name)
        except AssertionError:
            raise
