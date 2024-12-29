from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User
from apps.users.services import UserService


class RegisterSerializer(serializers.ModelSerializer):
    rewrite_password = serializers.CharField()

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
            "rewrite_password": {"write_only": True},
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
        rewrite_password = validated_data.pop("rewrite_password")
        self.service.create_user(
            **validated_data,
        )
        validated_data["rewrite_password"] = rewrite_password

        return validated_data


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email

        return token


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = UserService()

    def validate_email(self, email):
        if not self.service.get_user_by_email(email=email):
            raise serializers.ValidationError("User with this email does not exist")
        return email

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = self.service.authenticate_user(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Wrong credentials")

        refresh_token = TokenSerializer.get_token(user)
        access_token = refresh_token.access_token  # type: ignore

        attrs["access_token"] = access_token
        attrs["refresh_token"] = refresh_token

        return attrs


# class RefreshTokenSerializer(serializers.Serializer):
#     refresh = serializers.CharField(write_only=True)
#
#     def validate_refresh(self, value):  # noqa
#         try:
#
#
#             return refresh_token
#         except Exception:
#             raise serializers.ValidationError("Invalid refresh token.")