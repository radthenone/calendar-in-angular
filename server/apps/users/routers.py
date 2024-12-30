from django.urls import path

from apps.users.views import ChangePasswordViewSet

users_router = [
    path(
        "change-password/",
        ChangePasswordViewSet.as_view(),
        name="change-password",
    ),
]
