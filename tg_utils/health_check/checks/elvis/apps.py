from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = "tg_utils.health_check.checks.elvis"

    def ready(self):
        # pylint: disable=import-outside-toplevel
        from .backends import ElvisProxyHealthCheck

        plugin_dir.register(ElvisProxyHealthCheck)
