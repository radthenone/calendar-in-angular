import uuid
from typing import TYPE_CHECKING, Optional

import jwt
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

if TYPE_CHECKING:
    from apps.users.models import User


class UserManager(BaseUserManager):
    def get_user_by_id(self, user_id: uuid.UUID) -> Optional["User"]:
        try:
            return self.get(id=user_id)
        except self.model.DoesNotExist:
            return None

    def get_user_by_email(self, email: str) -> Optional["User"]:
        try:
            return self.get(email=email)
        except self.model.DoesNotExist:
            return None

    def get_user_by_id_and_email(
        self, user_id: uuid.UUID, email: str
    ) -> Optional["User"]:
        try:
            return self.get(id=user_id, email=email)
        except self.model.DoesNotExist:
            return None

    def create_user(
        self, email: str, password: str, **extra_fields
    ) -> Optional["User"]:
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

    def update_user(self, user_id: uuid.UUID, **kwargs) -> Optional["User"]:
        try:
            user = self.get(id=user_id)
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.save()
            return user
        except self.model.DoesNotExist:
            return None

    def delete_user(self, user_id: uuid.UUID) -> bool:
        try:
            user = self.get(id=user_id)
            user.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def last_login_update(
        self,
        user_id: uuid.UUID,
    ) -> None:
        user = self.get(id=user_id)
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

    def get_all_users(self) -> QuerySet["User"]:
        return self.all()

    def get_all_users_filter_by_last_login(self) -> QuerySet["User"]:
        return self.filter(last_login__isnull=False).order_by("-last_login")

    def update_password(
        self, user_id: uuid.UUID, new_password: str
    ) -> Optional["User"]:
        user = self.get_user_by_id(user_id)
        user.set_password(new_password)
        user.save()

        return user


class AuthManager(models.Manager):
    def authenticate_user(self, email, password) -> Optional["User"]:
        try:
            user = self.get(email=email)
        except self.model.DoesNotExist:
            return None
        if user.check_password(password) and user.is_active:
            return user
        return None

    @staticmethod
    def decode_token(token: AccessToken | RefreshToken) -> Optional[dict[str, any]]:
        try:
            payload = jwt.decode(
                str(token),
                key=settings.SECRET_KEY,
                algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidSignatureError:
            return None
