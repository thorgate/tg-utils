from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from tg_utils.health_check.base_checks import HTTPBasedHealthCheck


class ElvisProxyHealthCheck(HTTPBasedHealthCheck):
    """Check if it is possible to establish HTTP connection to Elvis proxy"""
    expected_status_code = 400

    def get_url(self):
        try:
            return settings.ELVIS_HOST
        except AttributeError:
            raise ImproperlyConfigured("To use Elvis Proxy health-check, set ELVIS_HOST in your settings.")
