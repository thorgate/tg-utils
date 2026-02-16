from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from health_check.exceptions import ServiceUnavailable
from tg_utils.health_check.base_checks import HealthCheckSettingsMixin, HealthCheck

CACHE_KEY = "CELERY_BEAT_HEALTH_CHECK_TIME_STAMP"
TIMEOUT = getattr(settings, "HEALTH_CHECK", {}).get("CELERY_BEAT_CHECK_INTERVAL", 60)
DELAY_THRESHOLD = getattr(settings, "HEALTH_CHECK", {}).get(
    "CELERY_BEAT_DELAY_THRESHOLD", 10
)


class CeleryBeatHealthCheck(HealthCheck, HealthCheckSettingsMixin):
    def check_status(self):
        last_beat_time = cache.get(CACHE_KEY, None)
        if last_beat_time is None:
            self.add_error(ServiceUnavailable("Celery beat is not scheduling tasks"))
            return

        if (
            not isinstance(last_beat_time, timezone.datetime)
            or not last_beat_time.tzinfo
        ):
            self.add_error(
                # If you encounter this error in tests, most likely you are using a fixture
                # instead of running the task, and the fixture is providing unaware timestamp. Switch
                # your ficture to locale-aware timestamp to fix this
                ServiceUnavailable(
                    f"Celery beat task timestamp is invalid: {last_beat_time!r}"
                )
            )
            return

        if (timezone.now() - last_beat_time).seconds > DELAY_THRESHOLD:
            self.add_error(
                ServiceUnavailable(
                    f"Celery beat tasks are delayed, last ran at {last_beat_time}."
                )
            )
