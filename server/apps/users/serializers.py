from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.users.models import User
from apps.users.services import UserService


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = UserService()

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("rewrite_new_password"):
            raise serializers.ValidationError("Passwords do not match")

        if attrs.get("old_password") == attrs.get("new_password"):
            raise serializers.ValidationError("New password is the same as old one")

        return attrs

    def validate_new_password(self, value):  # noqa
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def update(self, instance, validated_data):
        instance = self.service.update_password(
            user=instance,
            new_password=validated_data.get("new_password"),
        )
        return instance
