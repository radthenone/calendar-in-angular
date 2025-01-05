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
        return self.model.objects.filter(user=self.user).prefetch_related("dates").all()

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
