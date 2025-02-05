from django.urls import path

from apps.events.views import (
    EventCreateView,
    EventDetailView,
    EventListView,
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
    # path(
    #     "by-name/<str:name>/",
    #     EventDetailView.as_view(),
    #     name="event-detail-by-name",
    # ),
    # path(
    #     "by-date/<int:day>/<int:month>/<int:year>/",
    #     EventDetailView.as_view(),
    #     name="event-detail-by-date",
    # ),
    path(
        "<str:event_id>/",
        EventDetailView.as_view(),
        name="event-delete",
    ),
]
