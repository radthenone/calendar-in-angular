import logging
import uuid
from typing import TYPE_CHECKING, Optional

import jwt
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

if TYPE_CHECKING:
    from apps.users.models import User


logger = logging.getLogger(__name__)


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

    def create_user(self, email: str, password: str, **kwargs) -> Optional["User"]:
        if not email:
            logger.error("The Email field must be set")
            raise ValidationError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        return self.create_user(email, password, **kwargs)

    def update_user(self, user_id: uuid.UUID, **kwargs) -> Optional["User"]:
        try:
            with transaction.atomic():
                user = self.model(id=user_id)

                if "password" in kwargs:
                    user.set_password(kwargs.pop("password"))

                if "email" in kwargs:
                    user.email = self.normalize_email(kwargs.pop("email"))

                for key, value in kwargs.items():
                    setattr(user, key, value)

                user.save()
                return user

        except self.model.DoesNotExist:
            return None

        except Exception as e:
            logger.error(f"Error updating user: {e}")
            raise ValidationError(f"Error updating user: {e}")

    def delete_user(self, user_id: uuid.UUID) -> bool:
        try:
            user = self.get(id=user_id)
            user.delete()
            return True
        except self.model.DoesNotExist:
            raise ValidationError("User does not exist")

    def last_login_update(
        self,
        user_id: uuid.UUID,
    ) -> None:
        try:
            user = self.get(id=user_id)
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
        except self.model.DoesNotExist:
            raise ValidationError("User does not exist")

    def get_all_users(self) -> QuerySet["User"]:
        return self.all()

    def get_all_users_filter_by_last_login(self) -> QuerySet["User"]:
        return self.filter(last_login__isnull=False).order_by("-last_login")

    def update_password(
        self,
        user_id: uuid.UUID,
        new_password: str,
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
            raise ValidationError("User does not exist")

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
