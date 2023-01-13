import importlib

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from health_check.plugins import plugin_dir
from tg_utils.health_check.checks.celery_beat.backends import TIMEOUT
from tg_utils.health_check.checks.celery_beat.tasks import timestamp_task


class HealthCheckConfig(AppConfig):
    name = "tg_utils.health_check.checks.celery_beat"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from .backends import CeleryBeatHealthCheck

        cls = getattr(settings, "HEALTH_CHECK", {}).get("CELERY_APP", None)
        if cls is None:
            raise ImproperlyConfigured(
                "Set HEALTH_CHECK['CELERY_APP'] to point to celery app instance in your settings to use celery "
                "beat health-check (example value: 'my_project.celery.app')"
            )

        module_name, class_name = cls.rsplit(".", 1)
        app_module = importlib.import_module(module_name)

        signature_extra_kwargs = getattr(settings, "HEALTH_CHECK", {}).get(
            "CELERY_BEAT_SIGNATURE_EXTRA_KWARGS", {}
        )

        # Set initial timestamp not to fail the health-check before it runs for the first time
        # Don't use apply_async - otherwise, the whole initialisation will fail if celery fails
        try:
            timestamp_task()

            getattr(app_module, class_name).add_periodic_task(
                TIMEOUT,
                timestamp_task.signature((), **signature_extra_kwargs),
                name="Celery health check beat",
            )
        except Exception:
            # This is likely issue with the cache or with celery broker connection. Handle any exception not to let the
            # whole app go down - depending on cache and broker backend, different exceptions can be encountered here
            #
            # Don't try to recover from this error, health-check will be failing unless the issue is resolved.
            #
            # Don't log the exception since sometimes it is expected to fail here - i.e. when running some management
            # command that does not expect all the infrastructure to work
            pass

        plugin_dir.register(CeleryBeatHealthCheck)
