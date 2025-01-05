import uuid

from django.db import models

from apps.events.enums import RecurringType

# Create your models here.


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="events",
    )

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    recurring_type = models.CharField(
        max_length=50,
        choices=RecurringType.choices(),
        default=RecurringType.DAILY,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_event_name_per_user",
            )
        ]

    def __str__(self):
        return self.name


class EventDate(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="dates",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.event.name}: {self.start_datetime} - {self.end_datetime}"
