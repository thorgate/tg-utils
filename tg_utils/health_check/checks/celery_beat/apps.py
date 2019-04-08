import importlib

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from health_check.plugins import plugin_dir
from tg_utils.health_check.checks.celery_beat.backends import TIMEOUT
from tg_utils.health_check.checks.celery_beat.tasks import timestamp_task


class HealthCheckConfig(AppConfig):
    name = 'tg_utils.health_check.checks.celery_beat'

    def ready(self):
        from .backends import CeleryBeatHealthCheck

        cls = getattr(settings, 'HEALTH_CHECK', {}).get('CELERY_APP', None)
        if cls is None:
            raise ImproperlyConfigured(
                "Set HEALTH_CHECK['CELERY_APP'] to point to celery app instance in your settings to use celery "
                "beat health-check (example value: 'my_project.celery.app')"
            )

        module_name, class_name = cls.rsplit(".", 1)
        app_module = importlib.import_module(module_name)

        plugin_dir.register(CeleryBeatHealthCheck)
        getattr(app_module, class_name).add_periodic_task(TIMEOUT, timestamp_task.s(), name='Celery health check beat')
