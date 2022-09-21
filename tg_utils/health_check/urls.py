from django.urls import path

from tg_utils.health_check.views import HealthCheckViewProtected, HealthCheckViewMinimal


urlpatterns = [
    path(
        "health/detail/", HealthCheckViewProtected.as_view(), name="health-check-detail"
    ),
    path("health/", HealthCheckViewMinimal.as_view(), name="health-check"),
]
