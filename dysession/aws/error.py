from typing import Optional

from dysession.logger import get_logger


class DynamodbTableNotFound(Exception):
    def __init__(self, table_name: Optional[str] = None, *args: object) -> None:
        super().__init__(*args)

        logger = get_logger()
        if table_name:
            logger.error(f"'{table_name}' is not found in current region.")


class DynamodbItemNotFound(Exception):
    pass
