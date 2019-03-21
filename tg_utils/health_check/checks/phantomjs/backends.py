from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from tg_utils.health_check.base_checks import HTTPBasedHealthCheck


class PhantomJSHealthCheck(HTTPBasedHealthCheck):
    """Check if phantomJS pdf generator does not fail with error"""
    expected_status_code = 200
    method = 'POST'

    def get_payload(self):
        html = """
            <html>
                <body>
                    <h1>Health is important</h1>
                    <div>
                        If you are a developer reading this, take a 5 minute break to walk around now,
                        and prolong your life.
                    </div>
                </body>
            </html>
        """

        return {
            'html': html,
        }

    def get_url(self):
        try:
            return settings.PHANTOMJS_URL
        except AttributeError:
            raise ImproperlyConfigured("To use PhantomJS health-check, set PHANTOMJS_URL in your settings.")


class PhantomJSWithHeaderHtmlHealthCheck(PhantomJSHealthCheck):
    """Check if phantomJS pdf generator (version accepting both header_html and html) does not fail with error"""
    def get_payload(self):
        post_data = super().get_payload()
        post_data.update({
            'header_html': "<h2>The PDF Generator proudly presents</h2>"
        })
        return post_data
