from django.conf import settings
from django.core.checks import Warning


def check_production_settings(app_configs, **kwargs):
    issues = []

    if settings.DEBUG:
        return issues

    if not settings.EMAIL_HOST_PASSWORD or 'TODO' in settings.EMAIL_HOST_PASSWORD:
        issues.append(
            Warning(
                "EMAIL_HOST_PASSWORD setting is not set to proper value",
                id='tg_utils.W001',
            )
        )

    if 'TODO' in settings.SITE_URL:
        issues.append(
            Warning(
                "SITE_URL setting is not set to proper value",
                id='tg_utils.W002',
            )
        )

    return issues


def check_sentry_config(app_configs, **kwargs):
    issues = []

    if 'sentry' not in settings.LOGGING['handlers']:
        return issues

    if 'sentry' not in settings.LOGGING['loggers']['']['handlers']:
        issues.append(
            Warning(
                "Sentry logging handler is present but unused",
                hint="Ensure that sentry handler is part of LOGGING['loggers']['']['handlers']",
                id='tg_utils.W011',
            )
        )

    return issues
