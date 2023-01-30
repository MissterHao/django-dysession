from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser
from dysession.aws.dynamodb import destory_dynamodb_table

from dysession.settings import get_config


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
            "--region",
            type=str,
            default=config["DYNAMODB_REGION"],
            help="<Opitonal> Indicate to clear specified user's session data.",
            required=False,
        )
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        destory_dynamodb_table(options=options)
