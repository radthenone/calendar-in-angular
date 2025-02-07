import csv
import logging

from django.contrib.auth.hashers import make_password
from dotenv import load_dotenv
from faker import Faker

from apps.users.models import User
from config.paths import PROJECT_DIR

load_dotenv(
    dotenv_path=PROJECT_DIR / ".env.local",
)
logger = logging.getLogger(__name__)
fake = Faker()


def run(*args):
    _limit = 100
    _path = None

    for arg in args:
        if arg.startswith("limit="):
            _limit = int(arg.split("=")[1])
        elif arg.startswith("path="):
            _path = arg.split("=")[1]

    def contex_manager_csv(file_path: str) -> list[dict]:
        make_user = type(
            "MakeUser",
            (object,),
            {
                "__init__": lambda self, email, password: setattr(self, "email", email)
                or setattr(self, "password", password)
            },
        )
        rows = []
        with open(file_path, "r") as file:
            csv_file = csv.reader(file)
            next(csv_file)
            for row in csv_file:
                rows.append(make_user(email=f"{row[0]}", password=f"{row[1]}"))

        return rows

    def generate_users_list(limit: int = 100, file_path: str = None) -> list["User"]:
        _users = []
        if file_path:
            data = contex_manager_csv(file_path)
            for user in data:
                password = make_password(user.password)  # noqa
                _users.append(
                    User(
                        email=user.email,  # noqa
                        password=password,
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                    )
                )
        else:
            raw_password = make_password("Test1234!")
            for _ in range(limit):
                _users.append(
                    User(
                        email=fake.unique.email(),
                        password=raw_password,
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                    )
                )
        return _users

    def generate_users(users_list: list["User"]):
        User.objects.bulk_create(users_list)

    users = generate_users_list(limit=_limit, file_path=_path)
    generate_users(users_list=users)

    logger.info("Users created with password: Test1234!")
