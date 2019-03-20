from django.conf.urls import url

from tg_utils.health_check.views import HealthCheckViewProtected, HealthCheckViewMinimal


urlpatterns = [
    url(r'^health/detail/?$', HealthCheckViewProtected.as_view(), name='health-check-detail'),
    url(r'^health/?$', HealthCheckViewMinimal.as_view(), name='health-check'),
]
