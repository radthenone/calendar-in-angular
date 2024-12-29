from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.users.serializers import (
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
)
from apps.users.services import UserService


class RegisterViewSet(viewsets.ViewSet):
    service = UserService()
    queryset = service.get_all_users()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        examples=[
            OpenApiExample(
                "Register example",
                value={
                    "email": "example@example.com",
                    "password": "examplePassword123",
                    "rewrite_password": "examplePassword123",
                },
            )
        ],
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    service = UserService()
    queryset = service.get_all_users()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        examples=[
            OpenApiExample(
                "Login example",
                value={
                    "email": "example@example.com",
                    "password": "examplePassword123",
                },
            )
        ],
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            return Response(
                {"access": str(access_token), "refresh": str(refresh_token)},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class TokenRefreshViewSet(viewsets.ViewSet):
#     serializer_class = RefreshTokenSerializer
#     permission_classes = [AllowAny]
#
#     @extend_schema(
#         request=RefreshTokenSerializer,
#         examples=[
#             OpenApiExample(
#                 "Refresh token example",
#                 value={"refresh": "exampleRefreshToken123"},
#             )
#         ],
#     )
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             refresh_token: RefreshToken = serializer.validated_data["refresh"]
#             access_token = refresh_token.access_token
#             return Response(
#                 {"access": str(access_token), "refresh": str(refresh_token)},
#                 status=status.HTTP_200_OK,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
