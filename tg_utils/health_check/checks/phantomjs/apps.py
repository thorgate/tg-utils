from django.apps import AppConfig
from django.conf import settings

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'tg_utils.health_check.checks.phantomjs'

    def ready(self):
        from .backends import PhantomJSHealthCheck, PhantomJSWithHeaderHtmlHealthCheck

        if hasattr(settings, 'HEALTH_CHECK') and settings.HEALTH_CHECK.get('PHANTOMJS_REQUIRES_HEADER_HTML', False):
            plugin_dir.register(PhantomJSWithHeaderHtmlHealthCheck)
        else:
            plugin_dir.register(PhantomJSHealthCheck)
