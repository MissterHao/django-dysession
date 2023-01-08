import boto3
from ..settings import get_config
from typing import Any, Dict, Optional, Union


def create_dynamodb_table(options: Dict[str, Union[str, int]], client=None) -> Dict:
    
    if client is None:
        client = boto3.client("dynamodb")

    response = client.create_table(
        AttributeDefinitions=[
            # {"AttributeName": options["ttl"], "AttributeType": "N"},
            {"AttributeName": options["pk"], "AttributeType": "S"},
            {"AttributeName": options["sk"], "AttributeType": "S"},
        ],
        TableName=options["table"],
        KeySchema=[
            {"AttributeName": options["pk"], "KeyType": "HASH"},
            {"AttributeName": options["sk"], "KeyType": "RANGE"},
        ],
        BillingMode="PAY_PER_REQUEST",
        TableClass="STANDARD",
    )

    return response

def destory_dynamodb_table(options: Dict[str, Union[str, int]], client=None) -> Dict:
    
    if client is None:
        client = boto3.client("dynamodb")

    response = client.delete_table(TableName=options["table"])
    return response