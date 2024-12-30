from rest_framework.routers import DefaultRouter

from apps.auth.views import LoginViewSet, RegisterViewSet, TokenRefreshViewSet

auth_router = DefaultRouter()

auth_router.register("register", RegisterViewSet, basename="register")
auth_router.register("login", LoginViewSet, basename="login")
auth_router.register("refresh", TokenRefreshViewSet, basename="refresh-token")
