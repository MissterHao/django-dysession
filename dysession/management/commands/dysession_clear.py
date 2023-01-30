from typing import Any, Optional
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser


__all__ = ["Command"]


class Command(BaseCommand):

    help = "Clear all session record which stored in DynamoDB"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-u",
            "--uid",
            action="append",
            help="<Opitonal> Indicate to clear specified user's session data.",
            required=False,
        )
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        userids = options.get("uid", None)
        if userids:
            print(f"Ready to clear {userids} session data.")
            return

        print("Clearing whole session data")
        return 

