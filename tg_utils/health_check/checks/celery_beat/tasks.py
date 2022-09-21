from django.core.cache import cache
from django.utils.datetime_safe import datetime

from celery import shared_task  # pylint: disable=import-error
from tg_utils.health_check.checks.celery_beat.backends import CACHE_KEY


@shared_task(ignore_result=False)
def timestamp_task():
    # timeout=None causes value to be stored forever
    cache.set(CACHE_KEY, datetime.now(), timeout=None)
