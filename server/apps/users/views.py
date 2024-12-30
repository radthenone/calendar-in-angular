from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import (
    ChangePasswordSerializer,
)
from apps.users.services import UserService


class ChangePasswordViewSet(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_queryset(self):
        return UserService().get_all_users()

    def get_object(self):
        return self.request.user

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
