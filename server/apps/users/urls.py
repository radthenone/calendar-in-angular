from django.urls import path

from apps.users.views import (
    ChangePasswordView,
    UserDetailView,
    UserListView,
)

urlpatterns = [
    path(
        "",
        UserListView.as_view(),
        name="users-list",
    ),
    path(
        "<str:pk>/",
        UserDetailView.as_view(),
        name="user-detail",
    ),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
]
