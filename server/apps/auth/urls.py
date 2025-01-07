from django.urls import path

from apps.auth.views import LoginViewSet, RegisterView, TokenRefreshViewSet

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginViewSet.as_view({"post": "create"}), name="login"),
    path(
        "refresh-token/",
        TokenRefreshViewSet.as_view({"post": "create"}),
        name="refresh-token",
    ),
]
