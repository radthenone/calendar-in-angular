from django.urls import path

from apps.auth.views import LoginViewSet, RegisterViewSet, TokenRefreshViewSet

auth_router = [
    path("register/", RegisterViewSet.as_view({"post": "create"}), name="register"),
    path("login/", LoginViewSet.as_view({"post": "create"}), name="login"),
    path(
        "refresh-token/",
        TokenRefreshViewSet.as_view({"post": "create"}),
        name="refresh-token",
    ),
]
