import logging
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction

if TYPE_CHECKING:
    from apps.events.models import Event
    from apps.users.models import User

logger = logging.getLogger(__name__)


class EventManager(models.Manager):
    def get_event(self, event_id: uuid.UUID) -> Optional["Event"]:
        try:
            return self.get(id=event_id)
        except self.model.DoesNotExist:
            return None

    def is_exists(self, user: "User" = None, name: str = None, **kwargs) -> bool:
        return self.filter(user=user, name=name, **kwargs).exists()

    def create_event(
        self,
        user: "User",
        name: str,
        description: str,
        recurring_type: str,
        start_datetime: datetime,
        end_datetime: datetime,
        **kwargs,
    ) -> Optional["Event"]:
        try:
            with transaction.atomic():
                if self.is_exists(user=user, name=name):
                    logger.warning(
                        f"User {user.id} try to create event with name {name}"
                    )
                    raise ValidationError("Event with this name already exists.")

                event = self.create(
                    user=user,
                    name=name,
                    description=description,
                    recurring_type=recurring_type,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    **kwargs,
                )
                logger.info(f"User {user.id} created event with name {name}.")
                return event
        except Exception as error:
            logger.error(f"User {user.id} failed to create event with name {name}.")
            raise ValidationError(f"Failed to create event: {error}")

    def update_event(
        self,
        event_id: uuid.UUID,
        user: "User",
        name: Optional[str] = None,
        description: Optional[str] = None,
        recurring_type: Optional[str] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        **kwargs,
    ) -> Optional["Event"]:
        try:
            with transaction.atomic():
                update_fields = []
                event: "Event" = self.get(id=event_id)
                if not event:
                    logger.error(f"Event with id {event_id} does not exist.")
                    raise ValidationError("Event with this id does not exist.")

                if name is not None and event.name != name:
                    event.name = name
                    update_fields.append("name")

                if description is not None and event.description != description:
                    event.description = description
                    update_fields.append("description")

                if (
                    recurring_type is not None
                    and event.recurring_type != recurring_type
                ):
                    if recurring_type not in Event.RecurringType.values:
                        raise ValidationError("Invalid recurring type")
                    event.recurring_type = recurring_type
                    update_fields.append("recurring_type")

                if (
                    start_datetime is not None
                    and event.start_datetime != start_datetime
                ):
                    event.start_datetime = start_datetime
                    update_fields.append("start_datetime")

                if end_datetime is not None and event.end_datetime != end_datetime:
                    event.end_datetime = end_datetime
                    update_fields.append("end_datetime")

                for field, value in kwargs.items():
                    if getattr(event, field) != value:
                        setattr(event, field, value)
                        update_fields.append(field)

                if update_fields:
                    event.save(update_fields=update_fields)
                    logger.info(
                        f"User {user.id} updated event {event_id}. Updated fields: {update_fields}"
                    )
                else:
                    logger.info(f"No changes detected for event {event_id}")

                return event
        except Event.DoesNotExist:
            logger.error(f"Event with id {event_id} does not exist.")
            raise ValidationError("Event does not exist.")
        except IntegrityError:
            logger.error(f"Event with id {event_id} already exists.")
            raise ValidationError("Event already exists.")
        except Exception as error:
            logger.error(f"Failed to update event with id {event_id}.")
            raise ValidationError(f"Failed to update event: {error}")

        return None

    def delete_event(self, event_id: uuid.UUID) -> bool:
        event = self.get(id=event_id)
        if not event:
            logger.error(f"Event with id {event_id} does not exist.")
            raise ValidationError("Event does not exist.")

        try:
            event.delete()
            logger.info(f"Event with id {event_id} deleted.")
            return True
        except Exception as error:
            logger.error(f"Failed to delete event with id {event_id}.")
            raise ValidationError(f"Failed to delete event: {error}")
