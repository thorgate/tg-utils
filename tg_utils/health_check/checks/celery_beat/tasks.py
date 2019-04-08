from django.core.cache import cache
from django.utils.datetime_safe import datetime

from celery import shared_task
from tg_utils.health_check.checks.celery_beat.backends import (CACHE_KEY,
                                                               TIMEOUT)


@shared_task(ignore_result=False)
def timestamp_task():
    cache.set(CACHE_KEY, datetime.now(), timeout=TIMEOUT*2)
