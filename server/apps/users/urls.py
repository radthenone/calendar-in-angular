from django.urls import path

from apps.users.views import ChangePasswordView, UserListView

urlpatterns = [
    path(
        "",
        UserListView.as_view(),
        name="users-list",
    ),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
]
