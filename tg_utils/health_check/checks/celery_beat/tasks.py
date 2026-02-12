from django.core.cache import cache
from django.utils import timezone

import warnings
import functools

try:
    from celery import shared_task  # pylint: disable=import-error
except ImportError:

    def shared_task(*args, **kwargs):
        def decorator(func):
            @functools.wraps(func)
            def fake_task():
                warnings.warn(
                    "It seems that you do not have celery installed. "
                    "Celery beat health check will always report error.",
                    RuntimeWarning,
                )

            return fake_task

        return decorator


from tg_utils.health_check.checks.celery_beat.backends import CACHE_KEY


@shared_task(ignore_result=False)
def timestamp_task():
    # timeout=None causes value to be stored forever
    cache.set(CACHE_KEY, timezone.now(), timeout=None)
