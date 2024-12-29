from rest_framework.routers import DefaultRouter

from apps.users.views import LoginViewSet, RegisterViewSet

users_router = DefaultRouter()

users_router.register("register", RegisterViewSet, basename="register")
users_router.register("login", LoginViewSet, basename="login")
# users_router.register("refresh", TokenRefreshViewSet, basename="refresh-token")
