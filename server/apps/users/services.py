from typing import Optional

from django.contrib.auth.hashers import check_password, make_password

from apps.users.models import User


class UserService:
    def __init__(self):
        self.model = User

    def get_all_users(self):
        return self.model.objects.all()

    def get_all_users_filter_by_last_login(self):
        return self.model.objects.filter(last_login__isnull=False).order_by(
            "-last_login"
        )

    def get_user(self, user_id: int) -> User:
        return self.model.objects.get(id=user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.model.objects.filter(email=email).first()

    def check_password(self, user_id: int, password: str) -> bool:
        user = self.get_user(user_id=user_id)
        if not user:
            return False
        return check_password(password, user.password)

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

    @staticmethod
    def update_password(user: User, new_password: str) -> User:
        user.set_password(new_password)
        user.save()
        return user

    def delete_user(self, user_id: int):
        return self.model.objects.filter(id=user_id).delete()
