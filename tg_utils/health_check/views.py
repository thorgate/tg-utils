import logging

from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from health_check.views import MainView


logger = logging.getLogger('health')


class HealthCheckViewMinimal(MainView):
    """Always return json object, with single property `error` that is either true or false"""

    def render_to_response(self, context, **response_kwargs):
        status = response_kwargs.get('status', None)
        plugins = response_kwargs.get('plugins', None)
        return self.render_to_response_json(plugins, status)

    def render_to_response_json(self, plugins, status):
        return JsonResponse(
            {'error': status != 200},
            status=status,
        )


class HealthCheckViewProtected(MainView):
    """A comprehensive health-check view, accessible both in json and html table, protected with simple shared-secret
    based authentication"""

    def get(self, request, *args, **kwargs):
        access_token = getattr(settings, 'HEALTH_CHECK_ACCESS_TOKEN', None)
        header_name = getattr(settings, 'HEALTH_CHECK_ACCESS_TOKEN_HEADER', 'HTTP_X_HEALTHTOKEN')
        get_parameter_name = getattr(settings, 'HEALTH_CHECK_ACCESS_TOKEN_PARAMETER', 'healthtoken')
        if not access_token:
            logger.warning('Set %s in settings.py for health check protected view to work', header_name)
            return HttpResponseNotFound()
        if access_token not in [request.META.get(header_name), request.GET.get(get_parameter_name)]:
            return HttpResponseForbidden()

        return super().get(request, *args, **kwargs)
