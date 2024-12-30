from typing import Optional

from django.contrib.auth.hashers import make_password

from apps.users.models import User


class UserService:
    def __init__(self):
        self.model = User

    def get_all_users(self):
        return self.model.objects.all()

    def get_user(self, user_id: int) -> User:
        return self.model.objects.get(id=user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.model.objects.filter(email=email).first()

    def create_user(
        self,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> User:
        return self.model.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

    def create_superuser(
        self,
        email: str,
        password: str,
    ) -> User:
        return self.model.objects.create_superuser(
            email=email,
            password=password,
        )

    def update_user(self, user_id: int, **kwargs):
        return self.model.objects.filter(id=user_id).update(**kwargs)

    def update_password(self, user_id: int, new_password: str):
        new_hashed_password = make_password(new_password)
        return self.model.objects.filter(id=user_id).update(
            password=new_hashed_password
        )

    def delete_user(self, user_id: int):
        return self.model.objects.filter(id=user_id).delete()
