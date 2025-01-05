from django.urls import path

from apps.users.views import ChangePasswordViewSet, UserListViewSet

users_router = [
    path(
        "change-password/",
        ChangePasswordViewSet.as_view(),
        name="change-password",
    ),
    path(
        "list/",
        UserListViewSet.as_view(),
        name="users-list",
    ),
]
