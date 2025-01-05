from typing import Optional

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.auth.services import AuthService
from apps.users.models import User
from apps.users.services import UserService


class RegisterSerializer(serializers.ModelSerializer):
    rewrite_password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = UserService()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "rewrite_password",
            "first_name",
            "last_name",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("rewrite_password"):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def validate_email(self, value: str):  # noqa
        if "@" not in value:
            raise serializers.ValidationError("Invalid email")

        if self.service.get_user_by_email(email=value):
            raise serializers.ValidationError("User with this email already exists")
        return value

    def create(self, validated_data):
        validated_data.pop("rewrite_password")
        self.service.create_user(
            **validated_data,
        )

        return validated_data


class TokenSerializer(TokenObtainPairSerializer):
    auth_service = AuthService()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email

        return token

    @classmethod
    def get_refresh_token(cls, user) -> RefreshToken:
        refresh_token: RefreshToken = cls.get_token(user)  # type: ignore
        return refresh_token

    @classmethod
    def get_access_token(cls, user) -> AccessToken:
        access_token: AccessToken = cls.get_token(user).access_token  # type: ignore
        return access_token

    @classmethod
    def decode_token(
        cls, token: AccessToken | RefreshToken
    ) -> Optional[dict[str, any]]:
        try:
            return cls.auth_service.decode_token(token=token)
        except Exception:
            raise serializers.ValidationError("Invalid token")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = UserService()
        self.auth_service = AuthService()

    def validate_email(self, email):
        if not self.service.get_user_by_email(email=email):
            raise serializers.ValidationError("User with this email does not exist")
        return email

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = self.auth_service.authenticate_user(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Wrong credentials")

        self.auth_service.last_login_update(user=user)

        refresh_token = TokenSerializer.get_refresh_token(user)
        access_token = TokenSerializer.get_access_token(user)

        attrs["access_token"] = access_token
        attrs["refresh_token"] = refresh_token

        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = UserService()
        self.auth_service = AuthService()

    def validate(self, attrs):  # noqa
        token_error = "Invalid refresh token."
        payload = TokenSerializer.decode_token(attrs.get("refresh"))
        if payload is None:
            raise serializers.ValidationError(token_error)
        user = self.auth_service.check_user(
            email=payload.get("email"),
            user_id=payload.get("user_id"),
        )
        if not user:
            raise serializers.ValidationError(token_error)
        refresh_token = TokenSerializer.get_refresh_token(user)
        access_token = TokenSerializer.get_access_token(user)

        attrs["access_token"] = access_token
        attrs["refresh_token"] = refresh_token

        return attrs
