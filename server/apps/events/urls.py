from django.urls import path, re_path

from apps.events.views import (
    EventCreateView,
    EventDetailView,
    EventListView,
    EventMonthFilterListView,
)

urlpatterns = [
    path(
        "",
        EventListView.as_view(),
        name="events-list",
    ),
    path(
        "create/",
        EventCreateView.as_view(),
        name="event-create",
    ),
    path(
        "<str:event_id>/",
        EventDetailView.as_view(),
        name="event-detail",
    ),
    path(
        "<str:event_id>/",
        EventDetailView.as_view(),
        name="event-update",
    ),
    re_path(
        r"^(?P<year>\d{4})/(?P<month>\d{1,2})/$",
        EventMonthFilterListView.as_view(),
        name="event-month-filter",
    ),
    path(
        "<str:event_id>/",
        EventDetailView.as_view(),
        name="event-delete",
    ),
]
