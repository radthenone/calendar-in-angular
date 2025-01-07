from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.events.serializers import (
    EventCreateSerializer,
    EventSerializer,
)
from apps.events.services import EventService


class EventCreateView(generics.CreateAPIView):
    serializer_class = EventCreateSerializer

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["events"],
        request=EventCreateSerializer,
        examples=[
            OpenApiExample(
                "Create event example",
                value={
                    "name": "Example event",
                    "description": "Example description",
                    "recurring_type": "DAILY",
                    "start_date": "2025-01-05",
                    "start_time": "10:00:00",
                    "end_date": "2025-01-05",
                    "end_time": "18:00:00",
                },
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EventService(user=self.request.user).get_events()

    @extend_schema(
        tags=["events"],
        request=EventSerializer,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventDetailView(generics.GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_service = EventService(user=self.request.user)

        if "name" in self.kwargs:
            event = event_service.get_current_event_by_name(
                current_name=self.kwargs["name"]
            )
        elif all(key in self.kwargs for key in ("day", "month", "year")):
            event = event_service.get_current_event_by_date(
                current_day=self.kwargs["day"],
                current_month=self.kwargs["month"],
                current_year=self.kwargs["year"],
            )
        else:
            raise NotFound("Event not found.")

        if not event:
            raise NotFound("Event not found.")
        return event

    @extend_schema(
        tags=["events"],
        request=None,
        responses=EventSerializer,
        description=(
            "Retrieve an event by name or date. If 'name' is provided, it will retrieve "
            "by name. If 'day', 'month', and 'year' are provided, it will retrieve by date."
        ),
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class EventUpdateView(generics.UpdateAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_service = EventService(user=self.request.user)
        event = event_service.get_current_event_by_name(
            current_name=self.kwargs["name"]
        )
        if not event:
            raise NotFound("Event not found.")
        return event

    @extend_schema(
        tags=["events"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=["events"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class EventDeleteView(generics.DestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        event_service = EventService(user=self.request.user)
        event = event_service.get_current_event_by_name(
            current_name=self.kwargs["name"]
        )
        if not event:
            raise NotFound("Event not found.")
        return event

    @extend_schema(
        tags=["events"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
