from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    last_login_date = serializers.DateTimeField(format="%Y-%m-%d", source="last_login")
    last_login_time = serializers.DateTimeField(format="%H:%M:%S", source="last_login")

    class Meta:
        model = User
        fields = [
            "email",
            "last_login_date",
            "last_login_time",
        ]

        read_only_fields = [
            "id",
            "last_login_date",
            "last_login_time",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, source="password")
    new_password = serializers.CharField(required=True)
    rewrite_new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "old_password",
            "new_password",
            "rewrite_new_password",
        ]

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("rewrite_new_password"):
            raise serializers.ValidationError("Passwords do not match")

        if attrs.get("old_password") == attrs.get("new_password"):
            raise serializers.ValidationError("New password is the same as old one")

        return attrs

    def validate_new_password(self, value):  # noqa
        try:
            validate_password(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(list(error.messages))
        return value

    def update(self, instance, validated_data):
        instance = User.objects.update_password(
            user_id=instance.id,
            new_password=validated_data.get("new_password"),
        )
        return instance
