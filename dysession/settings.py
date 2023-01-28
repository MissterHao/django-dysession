from functools import lru_cache
from typing import Dict, Union

from django.conf import settings
from django.dispatch import receiver
from django.test.signals import setting_changed

DEFAULT_CONFIG = {
    "DYNAMODB_TABLENAME": "sessions",
    "PARTITION_KEY_NAME": "PK",
    "SORT_KEY_NAME": "SK",
    "TTL_ATTRIBUTE_NAME": "ttl",
    "CACHE_PERIOD": 3600,
    "DYNAMODB_REGION": "ap-northeast-1",
}


@lru_cache
def get_config() -> Dict[str, Union[str, int]]:
    config = DEFAULT_CONFIG.copy()
    custom_config = getattr(settings, "DYSESSION_CONFIG", {})
    config.update(custom_config)
    return config


@receiver(setting_changed)
def update_dysession_config(*, setting, **kwargs):
    if setting == "DYSESSION_CONFIG":  # pragma: no cover
        get_config.cache_clear()  # pragma: no cover


__all__ = ["get_config"]
