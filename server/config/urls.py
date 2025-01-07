from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="api-schema",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-redoc",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    re_path(
        r"^(?P<version>(v1|v2))/auth/",
        include("apps.auth.urls"),
        name="api-auth",
    ),
    re_path(
        r"^(?P<version>(v1|v2))/users/",
        include("apps.users.urls"),
        name="api-users",
    ),
    re_path(
        r"^(?P<version>(v1|v2))/events/",
        include("apps.events.urls"),
        name="api-events",
    ),
]
