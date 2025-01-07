import uuid
from datetime import date, datetime, time, timedelta

from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.timezone import get_current_timezone, make_aware

from apps.events.enums import RecurringType
from apps.events.models import Event, EventDate


class EventService:
    def __init__(self, user: AbstractBaseUser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.model = Event
        self.date_model = EventDate

    def get_events(self):
        if self.user.is_authenticated:
            return (
                self.model.objects.filter(user=self.user)
                .prefetch_related("dates")
                .all()
            )
        return self.model.objects.none()

    def get_current_event_by_date(
        self,
        current_day: int,
        current_month: int,
        current_year: int,
    ) -> Event:
        return (
            self.model.objects.filter(user=self.user)
            .filter(dates__start_datetime__day=current_day)
            .filter(dates__start_datetime__month=current_month)
            .filter(dates__start_datetime__year=current_year)
            .first()
        )

    def get_current_event_by_name(self, current_name: str) -> Event:
        return (
            self.model.objects.filter(user=self.user).filter(name=current_name).first()
        )

    def create_event_with_dates(
        self,
        name: str,
        description: str,
        recurring_type: RecurringType,
        start_date: date,
        start_time: time,
        end_date: date,
        end_time: time,
    ):
        event = self.model.objects.create(
            user=self.user,
            name=name,
            description=description,
            recurring_type=recurring_type,
        )

        dates = self._generate_event_dates(
            event,
            start_date,
            start_time,
            end_date,
            end_time,
        )

        self.date_model.objects.bulk_create(dates)

        return event

    def _generate_event_dates(
        self,
        instance: Event,
        start_date: date,
        start_time: time,
        end_date: date,
        end_time: time,
    ):
        dates = []
        current_date = start_date
        timezone = get_current_timezone()

        while current_date <= end_date:
            start_datetime = make_aware(
                datetime.combine(current_date, start_time), timezone=timezone
            )
            end_datetime = make_aware(
                datetime.combine(current_date, end_time), timezone=timezone
            )

            dates.append(
                self.date_model(
                    event=instance,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                )
            )

            if instance.recurring_type == RecurringType.DAILY.value:
                current_date += timedelta(days=1)
            elif instance.recurring_type == RecurringType.WEEKLY.value:
                current_date += timedelta(weeks=1)
            elif instance.recurring_type == RecurringType.MONTHLY.value:
                current_date = self._add_months(current_date, 1)
            elif instance.recurring_type == RecurringType.YEARLY.value:
                current_date = self._add_months(current_date, 12)
            else:
                break
        return dates

    @staticmethod
    def _add_months(source_date: date, months: int) -> date:
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(
            source_date.day,
            (datetime(year, month + 1, 1) - timedelta(days=1)).day,
        )
        return date(year, month, day)

    def update_event_with_dates(
        self,
        instance: Event,
        name: str = None,
        description: str = None,
        recurring_type: RecurringType = None,
        start_date: date = None,
        start_time: time = None,
        end_date: date = None,
        end_time: time = None,
    ):
        updated_fields = {}

        # Zaktualizowanie pól Event
        if name:
            updated_fields["name"] = name
        if description:
            updated_fields["description"] = description
        if recurring_type:
            updated_fields["recurring_type"] = recurring_type

        # Pobranie aktualnych dat z instancji Event
        current_start_datetime = instance.dates.first().start_datetime
        current_end_datetime = instance.dates.last().end_datetime

        # Sprawdzamy, czy dostarczono start_date lub start_time
        if start_date or start_time:
            new_start_datetime = make_aware(
                datetime.combine(
                    start_date or current_start_datetime.date(),
                    start_time or current_start_datetime.time(),
                ),
                timezone=get_current_timezone(),
            )
            updated_fields["dates__start_datetime"] = new_start_datetime
        else:
            # Jeśli nie zmienia się start_datetime, używamy wartości z instancji
            new_start_datetime = current_start_datetime

        # Sprawdzamy, czy dostarczono end_date lub end_time
        if end_date or end_time:
            new_end_datetime = make_aware(
                datetime.combine(
                    end_date or current_end_datetime.date(),
                    end_time or current_end_datetime.time(),
                ),
                timezone=get_current_timezone(),
            )
            updated_fields["dates__end_datetime"] = new_end_datetime
        else:
            # Jeśli nie zmienia się end_datetime, używamy wartości z instancji
            new_end_datetime = current_end_datetime

        # Sprawdzamy, czy start datetime jest wcześniejsze niż end datetime
        if new_start_datetime >= new_end_datetime:
            raise ValueError("Start datetime should be earlier than end datetime.")

        # Jeśli daty zostały zmienione, aktualizujemy EventDate
        if (
            "dates__start_datetime" in updated_fields
            or "dates__end_datetime" in updated_fields
        ):
            self.date_model.objects.bulk_update(
                instance.dates.all(),
                fields=[
                    "start_datetime",
                    "end_datetime",
                ],  # Tylko pola, które się zmieniły
            )

        # Zaktualizowanie samego Event
        instance.save(update_fields=updated_fields.keys())

        return instance
