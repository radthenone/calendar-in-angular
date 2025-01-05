from django.urls import path

from apps.events.views import (
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
)

events_router = [
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
        "<str:name>/",
        EventDetailView.as_view(),
        name="event-detail",
    ),
    path(
        "<int:day>/<int:month>/<int:year>/",
        EventDetailView.as_view(),
        name="event-detail",
    ),
    path(
        "<str:name>/delete/",
        EventDeleteView.as_view(),
        name="event-delete",
    ),
]
