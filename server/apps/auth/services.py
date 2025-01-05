from typing import Optional

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.users.models import User


class AuthService:
    def __init__(self):
        self.model = User

    def check_user(self, user_id: int, email: str) -> Optional[User]:
        return self.model.objects.filter(id=user_id, email=email).first()

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            return None
        if user is not None and user.check_password(password):
            if user.is_active:
                return user
        return None

    @staticmethod
    def last_login_update(user: User):
        user.last_login = timezone.now()
        user.save()

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
