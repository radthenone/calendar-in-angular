import uuid
from datetime import datetime

from django.db import models

from apps.events.enums import RecurringType
from apps.events.managers import EventManager


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)

    start_datetime = models.DateTimeField(default=datetime.now())
    end_datetime = models.DateTimeField()

    recurring_type = models.CharField(
        max_length=50,
        choices=RecurringType.choices(),
        default=RecurringType.DAILY,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="events",
    )

    objects = EventManager()

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"
        db_table = "events"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_event_name_per_user",
            )
        ]
        indexes = [models.Index(fields=["start_datetime", "end_datetime"])]

    def __str__(self):
        return f"Event: {self.name}"
