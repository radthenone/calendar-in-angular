from datetime import datetime

from django.db import transaction
from django.utils.timezone import get_current_timezone, make_aware
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema_field
from rest_framework import serializers, status

from apps.events.enums import RecurringType
from apps.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    start_date = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=["%Y-%m-%d"],
        write_only=True,
        required=True,
    )
    start_time = serializers.TimeField(
        format="%H:%M-%S",
        input_formats=["%H:%M"],
        write_only=True,
        required=True,
    )
    end_date = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=["%Y-%m-%d"],
        write_only=True,
        required=True,
    )
    end_time = serializers.TimeField(
        format="%H:%M-%S",
        input_formats=["%H:%M"],
        write_only=True,
        required=True,
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "recurring_type",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
            "start_datetime",
            "end_datetime",
            # nested fields
            "user",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["start_datetime"] = make_aware(
            datetime.combine(data["start_date"], data["start_time"]),
            timezone=get_current_timezone(),
        )
        data["end_datetime"] = make_aware(
            datetime.combine(data["end_date"], data["end_time"]),
            timezone=get_current_timezone(),
        )
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["start_date"] = instance.start_datetime.strftime(format="%Y-%m-%d")
        data["start_time"] = instance.start_datetime.strftime(format="%H:%M:%S")
        data["end_date"] = instance.end_datetime.strftime(format="%Y-%m-%d")
        data["end_time"] = instance.end_datetime.strftime(format="%H:%M:%S")
        return data

    def validate_recurring_type(self, value):  # noqa
        if value not in RecurringType.values():
            raise serializers.ValidationError("Invalid recurring type.")

    def validate(self, attrs):
        if attrs["start_datetime"] > attrs["end_datetime"]:
            raise serializers.ValidationError(
                detail="Start datetime should be earlier than end datetime.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        if attrs["start_datetime"] < datetime.now(tz=get_current_timezone()):
            raise serializers.ValidationError("Start datetime should be in the future.")

        return attrs

    def create(self, validated_data):
        user = validated_data.pop("user", None)
        if not user:
            raise serializers.ValidationError("User is required.")
        try:
            event = Event.objects.create_event(
                user=user,
                name=validated_data["name"],
                description=validated_data["description"],
                recurring_type=validated_data["recurring_type"],
                start_datetime=validated_data["start_datetime"],
                end_datetime=validated_data["end_datetime"],
                **validated_data,
            )
            return event
        except Exception as error:
            raise serializers.ValidationError(error)

    def update(self, instance, validated_data):
        user = validated_data.pop("user", None)
        if not user:
            raise serializers.ValidationError("User is required.")
        try:
            event = Event.objects.update_event(
                instance=instance,
                user=user,
                name=validated_data.get("name", instance.name),
                description=validated_data.get("description", instance.description),
                recurring_type=validated_data.get(
                    "recurring_type", instance.recurring_type
                ),
                start_datetime=validated_data.get(
                    "start_datetime", instance.start_datetime
                ),
                end_datetime=validated_data.get("end_datetime", instance.end_datetime),
                **validated_data,
            )
            return event
        except Exception as error:
            raise serializers.ValidationError(error)
