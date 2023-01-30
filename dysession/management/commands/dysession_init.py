from typing import Any, Optional

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from dysession.aws.dynamodb import create_dynamodb_table
from dysession.settings import get_config

from ._arg_types import positive_int

__all__ = ["Command"]


class Command(BaseCommand):

    help = "Clear all session record which stored in DynamoDB"

    def add_arguments(self, parser: CommandParser) -> None:
        config = get_config()
        parser.add_argument(
            "-n",
            "--table",
            type=str,
            default=config["DYNAMODB_TABLENAME"],
            help="<Opitonal> Indicate to clear specified user's session data.",
            required=False,
        )
        parser.add_argument(
            "--pk",
            action="append",
            default=config["PARTITION_KEY_NAME"],
            help="<Opitonal> Indicate to clear specified user's session data.",
            required=False,
        )
        parser.add_argument(
            "--sk",
            type=str,
            default=config["SORT_KEY_NAME"],
            help="<Opitonal> Indicate to clear specified user's session data.",
            required=False,
        )
        parser.add_argument(
            "--ttl",
            type=str,
            default=config["TTL_ATTRIBUTE_NAME"],
            help="<Opitonal> Indicate to clear specified user's session data.",
            required=False,
        )
        parser.add_argument(
            "--region",
            type=str,
            default=config["DYNAMODB_REGION"],
            help="<Opitonal> Indicate to clear specified user's session data.",
            required=False,
        )
        parser.add_argument(
            "--period",
            type=positive_int,
            default=config["CACHE_PERIOD"],
            help="<Opitonal> Indicate to clear specified user's session data.",
            required=False,
        )
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        create_dynamodb_table(options=options)
