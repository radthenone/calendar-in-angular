from typing import Optional

from django.utils import timezone
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.users.models import User


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email

        return token

    @classmethod
    def get_refresh_token(cls, user: "User") -> RefreshToken:
        refresh_token: RefreshToken = cls.get_token(user)  # type: ignore
        return refresh_token

    @classmethod
    def get_access_token(cls, user: "User") -> AccessToken:
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
            "password": {"required": True, "write_only": True},
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

        user = User.objects.create_user(**validated_data)
        from django.utils import timezone

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        user.access = TokenSerializer.get_refresh_token(user)
        user.refresh = TokenSerializer.get_access_token(user)

        return user

    def to_representation(self, instance):
        return {
            "access": str(instance.access),
            "refresh": str(instance.refresh),
            "user": {
                "id": instance.id,
                "email": instance.email,
            },
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_email(email: str) -> str:
        if not User.objects.get_user_by_email(email=email):
            raise serializers.ValidationError(
                detail="User with this email does not exist",
                code=status.HTTP_404_NOT_FOUND,
            )
        return email

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.auth.authenticate_user(email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                detail="Invalid credentials",
                code=status.HTTP_400_BAD_REQUEST,
            )

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        attrs["user"] = user
        attrs["access"] = TokenSerializer.get_refresh_token(user)
        attrs["refresh"] = TokenSerializer.get_access_token(user)
        return attrs

    def to_representation(self, instance):
        return {
            "access": str(instance["access"]),
            "refresh": str(instance["refresh"]),
            "user": {
                "id": instance["user"].id,
                "email": instance["user"].email,
            },
        }


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate(self, attrs):  # noqa
        payload = TokenSerializer.decode_token(attrs.get("refresh"))
        if payload is None:
            raise serializers.ValidationError(
                detail="Invalid refresh token",
                code=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.get_user_by_id_and_email(
            user_id=payload.get("user_id"),
            email=payload.get("email"),
        )
        if not user:
            raise serializers.ValidationError(
                detail="User not found",
                code=status.HTTP_404_NOT_FOUND,
            )

        attrs["user"] = user
        attrs["access"] = TokenSerializer.get_refresh_token(user)
        attrs["refresh"] = TokenSerializer.get_access_token(user)
        return attrs

    def to_representation(self, instance):
        return {
            "access": str(instance["access"]),
            "refresh": str(instance["refresh"]),
            "user": {
                "id": instance["user"].id,
                "email": instance["user"].email,
            },
        }
