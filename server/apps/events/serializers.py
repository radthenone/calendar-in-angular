from datetime import datetime

from django.db import transaction
from django.utils.timezone import get_current_timezone, make_aware
from rest_framework import serializers

from apps.events.models import Event, EventDate
from apps.events.services import EventService


class EventDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        fields = [
            "id",
            "start_datetime",
            "end_datetime",
        ]


class EventSerializer(serializers.ModelSerializer):
    dates = EventDaySerializer(many=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "recurring_type",
            "dates",
        ]


class EventCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_date = serializers.DateField()
    end_time = serializers.TimeField()

    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "recurring_type",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
        ]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        start_time = attrs.get("start_time")
        end_date = attrs.get("end_date")
        end_time = attrs.get("end_time")

        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)

        start_datetime = make_aware(start_datetime, timezone=get_current_timezone())
        end_datetime = make_aware(end_datetime, timezone=get_current_timezone())

        now = datetime.now(tz=get_current_timezone())

        if start_datetime > end_datetime:
            raise serializers.ValidationError(
                "Start datetime should be earlier than end datetime"
            )

        if start_datetime > end_datetime:
            raise serializers.ValidationError(
                "Start datetime should be earlier than end datetime"
            )

        if start_datetime < now:
            raise serializers.ValidationError("Start datetime should be in the future")

        return attrs

    def create(self, validated_data):
        service = EventService(user=self.context["request"].user)
        try:
            with transaction.atomic():
                service.create_event_with_dates(
                    name=validated_data["name"],
                    description=validated_data["description"],
                    recurring_type=validated_data["recurring_type"],
                    start_date=validated_data["start_date"],
                    start_time=validated_data["start_time"],
                    end_date=validated_data["end_date"],
                    end_time=validated_data["end_time"],
                )
        except Exception as error:
            raise serializers.ValidationError(error)
        return validated_data
