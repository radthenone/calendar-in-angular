import argparse
import logging
from datetime import timedelta
from random import choice, choices, randint

from django.db.models import QuerySet
from django.utils import timezone
from dotenv import load_dotenv
from faker import Faker

from apps.events.enums import RecurringType
from apps.events.models import Event
from apps.users.models import User
from config.paths import PROJECT_DIR

logger = logging.getLogger(__name__)

load_dotenv(
    dotenv_path=PROJECT_DIR / ".env.local",
)

fake = Faker()


def run(*args):
    def generate_events_list(
        users_list: QuerySet["User"], limit: int = 100
    ) -> list["Event"]:
        _events = []
        selected_users = choices(users_list, k=limit)

        for user in selected_users:
            start_datetime = fake.date_between(start_date="-126d", end_date="+126d")
            end_datetime = fake.date_between(start_date="-126d", end_date="+126d")
            while start_datetime > end_datetime:
                end_datetime = fake.date_between(start_date="-126d", end_date="+126d")

            _events.append(
                Event(
                    user=user,
                    name=fake.unique.name(),
                    description=fake.text(),
                    recurring_type=str(choice(RecurringType.choices())[0]),
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                )
            )

        return _events

    def generate_events(users_list: QuerySet["User"], limit: int = 100) -> None:
        events = generate_events_list(users_list=users_list, limit=limit)
        Event.objects.bulk_create(events)
        logger.info(f"Created {len(events)} events")

    users = User.objects.all()
    _limit = int(args[0]) if len(args) > 0 else 100
    generate_events(users_list=users, limit=_limit)
