from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import (
    ChangePasswordSerializer,
    UserListSerializer,
    UserSerializer,
)


class UserDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get_user_by_id(user_id=self.request.user.id)

    @extend_schema(
        tags=["users"],
        examples=[
            OpenApiExample(
                "Get user example",
                value={
                    "email": "example@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                },
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["users"],
        request=UserSerializer,
        examples=[
            OpenApiExample(
                "Update user example",
                value={
                    "email": "example@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                },
            )
        ],
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["users"],
        request=UserSerializer,
        examples=[
            OpenApiExample(
                "Update user example",
                value={
                    "email": "example@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                },
            )
        ],
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["users"],
    )
    def delete(self, request, *args, **kwargs):
        if User.objects.delete_user(user_id=self.request.user.id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [AllowAny]
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.get_all_users_filter_by_last_login()

    @extend_schema(
        tags=["users"],
        request=UserListSerializer,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ChangePasswordView(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return User.objects.get_user_by_id(user_id=self.request.user.id)

    @extend_schema(
        tags=["users"],
        request=ChangePasswordSerializer,
        examples=[
            OpenApiExample(
                "Change password example",
                value={
                    "old_password": "examplePassword123",
                    "new_password": "examplePassword1234",
                    "rewrite_new_password": "examplePassword1234",
                },
            )
        ],
    )
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            partial=True,
            instance=self.get_object(),
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
