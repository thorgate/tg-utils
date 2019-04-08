from django.conf import settings
from django.core.cache import cache
from django.utils.datetime_safe import datetime

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable
from tg_utils.health_check.base_checks import HealthCheckSettingsMixin


CACHE_KEY = "CELERY_BEAT_HEALTH_CHECK_TIME_STAMP"
TIMEOUT = getattr(settings, 'HEALTH_CHECK', {}).get('CELERY_BEAT_CHECK_INTERVAL', 60)
DELAY_THRESHOLD = getattr(settings, 'HEALTH_CHECK', {}).get('CELERY_BEAT_DELAY_THRESHOLD', 10)


class CeleryBeatHealthCheck(BaseHealthCheckBackend, HealthCheckSettingsMixin):
    def check_status(self):
        last_beat_time = cache.get(CACHE_KEY, None)
        if last_beat_time is None:
            self.add_error(ServiceUnavailable("Celery beat is not scheduling tasks"))
        elif (datetime.now() - last_beat_time).seconds > TIMEOUT + DELAY_THRESHOLD:
            self.add_error(ServiceUnavailable("Celery beat tasks are delayed"))
