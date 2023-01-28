from typing import Any, Optional


class SessionDataModel:
    def __init__(self, session_key: Optional[str]) -> None:
        self.session_key = session_key
        self.__variables_names = set()

    def __getitem__(self, key) -> Any:
        return getattr(self, key)

    def __setitem__(self, key, value):
        if key == "session_key":
            raise ValueError()

        setattr(self, key, value)
        self.__variables_names.add(key)

    def __delitem__(self, key):
        del self.__variables_names[key]
        delattr(self, key)

    def __iter__(self):
        return iter(self.__variables_names)

    def __is_empty(self):
        return len(self.__variables_names) == 0

    is_empty = property(__is_empty)

    def get(self, key, default=...):
        try:
            return self[key]
        except AttributeError:
            if default is Ellipsis:
                raise
            return default
    def pop(self, key, default):
        try:
            ret = self[key]
            del self[key]
            return ret
        except AttributeError:
            if default is Ellipsis:
                raise
            return default