import logging

import requests
from django.conf import settings
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceReturnedUnexpectedResult, ServiceUnavailable


logger = logging.getLogger('health')


class HealthCheckSettingsMixin:
    """Mixin that makes settings.HEALTH_CHECK available as property, and supplies empty dict instead if the setting
     is not defined"""
    @property
    def settings(self):
        return getattr(settings, 'HEALTH_CHECK', {})

    @property
    def requests_timeout(self):
        return self.settings.get('REQUESTS_TIMEOUT', 5)


class HTTPBasedHealthCheck(BaseHealthCheckBackend, HealthCheckSettingsMixin):
    """Helper class for any health check that check status of HTTP based service"""

    expected_status_code = 200
    method = 'GET'
    url = None
    payload = None

    def get_url(self):
        return self.url

    def get_method(self):
        return self.method

    def get_payload(self):
        return self.payload

    def check_status(self):
        try:
            response = requests.request(
                self.get_method(),
                self.get_url(),
                data=self.get_payload(),
                timeout=self.requests_timeout,
            )
        except requests.RequestException as e:
            logger.exception(e)
            self.add_error(ServiceUnavailable("{url} - {error}".format(
                url=self.url,
                error=e.__class__.__name__,
            )))
        else:
            if response.status_code != self.expected_status_code:
                self.add_error(ServiceReturnedUnexpectedResult("Expected {expected}, got {actual}".format(
                    expected=self.expected_status_code,
                    actual=response.status_code,
                )))
