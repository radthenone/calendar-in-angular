from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.auth.serializers import (
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
)


class RegisterView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["auth"],
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
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={
                    "detail": "User created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["auth"],
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
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # noqa
        if serializer.is_valid(raise_exception=True):
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            return Response(
                data={
                    "detail": "User logged in successfully",
                },
                headers={
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshViewSet(viewsets.ViewSet):
    serializer_class = RefreshTokenSerializer

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["auth"],
        request=RefreshTokenSerializer,
        examples=[
            OpenApiExample(
                "Refresh token example",
                value={"refresh": "exampleRefreshToken123"},
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)  # noqa
        if serializer.is_valid(raise_exception=True):
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            return Response(
                data={
                    "detail": "Token refreshed successfully",
                },
                headers={
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
