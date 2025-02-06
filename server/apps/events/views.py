import uuid
from datetime import datetime
from tkinter.scrolledtext import example

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, mixins, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Event
from apps.events.serializers import (
    EventSerializer,
)


class EventListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user:
            return Event.objects.filter(user=self.request.user)
        return Event.objects.none()

    @extend_schema(
        tags=["events"],
        request=EventSerializer,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventCreateView(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    @extend_schema(
        tags=["events"],
        request=EventSerializer,
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventDetailView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_object(self):
        event_id = self.kwargs.get("event_id")
        event = Event.objects.filter(user=self.request.user).get(id=uuid.UUID(event_id))

        if not event:
            raise NotFound("Event not found")

        return event

    @extend_schema(
        tags=["events"],
        request=EventSerializer,
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["events"],
        request=EventSerializer,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=["events"],
        request=EventSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=["events"],
        request=EventSerializer,
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EventMonthFilterListView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_queryset(self):
        today = datetime.now()

        user = self.request.user
        month = int(self.kwargs.get("month", today.month))
        year = int(self.kwargs.get("year", today.year))

        return Event.objects.filter_calendar_month_events(
            user=user,
            month=month,
            year=year,
        )

    @extend_schema(
        tags=["events"],
        request=EventSerializer,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
