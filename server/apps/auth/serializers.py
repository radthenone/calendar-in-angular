from typing import Optional

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    rewrite_password = serializers.CharField(write_only=True, required=True)

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
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
            "first_name": {"required": False, "write_only": True},
            "last_name": {"required": False, "write_only": True},
        }

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("rewrite_password"):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def validate_email(self, value: str):  # noqa
        if "@" not in value:
            raise serializers.ValidationError("Invalid email")

        if User.objects.get_user_by_email(email=value):
            raise serializers.ValidationError("User with this email already exists")
        return value

    def create(self, validated_data):
        validated_data.pop("rewrite_password")

        User.objects.create_user(**validated_data)
        return validated_data


class TokenSerializer(TokenObtainPairSerializer):
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
            return User.auth.decode_token(token=token)
        except Exception:
            raise serializers.ValidationError("Invalid token")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_email(email):
        if not User.objects.get_user_by_email(email=email):
            raise serializers.ValidationError("User with this email does not exist")
        return email

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.auth.authenticate_user(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Wrong credentials")

        User.objects.last_login_update(user_id=user.id)

        refresh_token = TokenSerializer.get_refresh_token(user)
        access_token = TokenSerializer.get_access_token(user)

        attrs["access_token"] = access_token
        attrs["refresh_token"] = refresh_token

        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate(self, attrs):  # noqa
        payload = TokenSerializer.decode_token(attrs.get("refresh"))
        if payload is None:
            raise serializers.ValidationError("Invalid refresh token")
        user = User.objects.get_user_by_id_and_email(
            user_id=payload.get("user_id"),
            email=payload.get("email"),
        )
        if not user:
            raise serializers.ValidationError("Invalid refresh token")
        refresh_token = TokenSerializer.get_refresh_token(user)
        access_token = TokenSerializer.get_access_token(user)

        attrs["access_token"] = access_token
        attrs["refresh_token"] = refresh_token

        return attrs
