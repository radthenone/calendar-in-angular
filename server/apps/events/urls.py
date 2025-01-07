from django.urls import path

from apps.events.views import (
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventUpdateView,
)

urlpatterns = [
    path(
        "list/",
        EventListView.as_view(),
        name="events-list",
    ),
    path(
        "create/",
        EventCreateView.as_view(),
        name="event-create",
    ),
    path(
        "<str:name>/update/",
        EventUpdateView.as_view(),
        name="event-update",
    ),
    path(
        "by-name/<str:name>/",
        EventDetailView.as_view(),
        name="event-detail-by-name",
    ),
    path(
        "by-date/<int:day>/<int:month>/<int:year>/",
        EventDetailView.as_view(),
        name="event-detail-by-date",
    ),
    path(
        "<str:name>/delete/",
        EventDeleteView.as_view(),
        name="event-delete",
    ),
]
