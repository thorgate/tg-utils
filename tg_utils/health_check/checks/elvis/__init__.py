import django

if django.VERSION < (3, 2):
    default_app_config = "tg_utils.health_check.checks.elvis.apps.HealthCheckConfig"
