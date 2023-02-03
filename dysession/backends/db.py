import logging
from typing import Any, Dict, Optional

import boto3
from django.contrib import auth
from django.contrib.sessions.backends.base import CreateError, SessionBase
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone

from dysession.aws.dynamodb import DynamoDB
from dysession.backends.error import (
    DeleteSessionError,
    SessionExpired,
    SessionKeyDoesNotExist,
    SessionKeyDuplicated,
)
from dysession.backends.model import SessionDataModel
from dysession.settings import get_config


class SessionStore(SessionBase):
    """Implement DynamoDB session store"""

    def __init__(self, session_key: Optional[str], **kwargs: Any) -> None:
        super().__init__(session_key, **kwargs)
        self.db = DynamoDB(
            client=boto3.client("dynamodb", region_name=get_config()["DYNAMODB_REGION"])
        )
        self._get_session()

    def _get_session_from_ddb(self) -> SessionDataModel:
        try:
            return self.db.get(session_key=self.session_key)
        except (SessionKeyDoesNotExist, SessionExpired, SuspiciousOperation) as e:
            if isinstance(e, SuspiciousOperation):
                logger = logging.getLogger(f"django.security.{e.__class__.__name__}")
                logger.warning(str(e))
            self._session_key = None

    def _get_session(self, no_load=False) -> SessionDataModel:
        """
        Lazily load session from storage (unless "no_load" is True, when only
        an empty dict is stored) and store it in the current instance.
        """
        self.accessed = True
        try:
            if isinstance(self._session_cache, SessionDataModel):
                return self._session_cache
            raise AttributeError
        except AttributeError:
            if self.session_key is None or no_load:
                self._session_cache = SessionDataModel(self.session_key)
            else:
                self._session_cache = self.load()
        return self._session_cache

    @property
    def key_salt(self):
        return "dysession.backends." + self.__class__.__qualname__

    def is_empty(self):
        "Return True when there is no session_key and the session is empty."
        try:
            return not self._session_key and not self._session_cache.is_empty
        except AttributeError:
            return True

    def clear(self):
        super().clear()
        self._session_cache = SessionDataModel()

    def items(self):
        return self._session.items()

    def __str__(self):
        return str(self._get_session())

    # Methods that subclass must implement
    def exists(self, session_key: str) -> bool:
        """
        Return True if the given session_key already exists.
        """
        return self.db.exists(session_key)

    def create(self) -> None:
        """
        Create a new session instance. Guaranteed to create a new object with
        a unique key and will have saved the result once (with empty data)
        before the method returns.
        """
        while True:
            self._session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the database.
                self.save(must_create=True)
            except (CreateError, SessionKeyDuplicated):
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            return

    def save(self, must_create: bool = False) -> None:
        """
        Save the session data. If 'must_create' is True, create a new session
        object (or raise CreateError). Otherwise, only update an existing
        object and don't create one (raise UpdateError if needed).
        """
        try:
            if self._session_key is None:
                return self.create()

            data = self._get_session(no_load=must_create)
            data.session_key = self._session_key
            self.db.set(data=data)
        except SessionKeyDuplicated:
            if must_create:
                raise SessionKeyDuplicated

    def delete(self, session_key=None):
        """
        Delete the session data under this key. If the key is None, use the
        current session key value.
        """
        if session_key is None:
            session_key = self._session_key

        print(f"On Delete: session_key: {session_key}")
        self.db.delete(self._get_session())
        
        try:
            pass
        except DeleteSessionError:
            print(f"On Delete Error: session_key: {session_key}")

    def load(self) -> SessionDataModel:
        """
        Load the session data and return a dictionary.
        """
        s = self._get_session_from_ddb()
        return s if s else SessionDataModel()

    @classmethod
    def clear_expired(cls) -> None:
        # clearing expired-items from dynamodb table is extremely expensive
        # Instead of clearing expired-items, we should use ttl attribube and which is much cost-effective
        ...
