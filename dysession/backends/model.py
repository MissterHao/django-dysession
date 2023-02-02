import json
from typing import Any, Optional


class SessionDataModel:

    NOTFOUND_ALLOW_LIST = ["_auth_user_id", "_auth_user_backend", "_auth_user_hash"]

    def __init__(self, session_key: Optional[str] = None) -> None:

        if type(session_key) is not str and session_key is not None:
            raise TypeError("session_key should be type str or None")

        self.session_key = session_key
        self.__variables_names = set(["session_key"])

    def __getitem__(self, key) -> Any:
        # Set SESSION_EXPIRE_AT_BROWSER_CLOSE to False
        # https://docs.djangoproject.com/en/4.1/topics/http/sessions/#browser-length-sessions-vs-persistent-sessions
        if key == "_session_expiry":
            return False

        try:
            return getattr(self, key)
        except AttributeError:
            if key in self.NOTFOUND_ALLOW_LIST:
                raise KeyError
            raise

    def __setitem__(self, key, value):
        # if key == "session_key":
        #     raise ValueError()

        setattr(self, key, value)
        self.__variables_names.add(key)

    def __delitem__(self, key):
        self.__variables_names.remove(key)
        delattr(self, key)

    def __iter__(self):
        return iter(self.__variables_names)

    def __is_empty(self):
        return "session_key" in self.__variables_names and len(self.__variables_names) == 1

    is_empty = property(__is_empty)

    def get(self, key, default=...):
        try:
            return self[key]
        except AttributeError:
            if key in self.NOTFOUND_ALLOW_LIST:
                return None

            if default is Ellipsis:
                raise
            return default

    def pop(self, key, default=...):
        try:
            ret = self[key]
            del self[key]
            return ret
        except AttributeError:
            if default is Ellipsis:
                raise
            return default

    def items(self):
        for key in self.__variables_names:
            yield (key, self[key])

    def __str__(self) -> str:
        data = {}
        for key in self.__variables_names:
            data[key] = getattr(self, key)

        return json.dumps(data)
