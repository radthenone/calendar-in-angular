from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiRequest,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.auth.serializers import (
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        tags=["auth"],
        request=OpenApiRequest(
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
        ),
        responses={
            201: OpenApiResponse(
                response=RegisterSerializer,
                description="Successfully registered",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "user": {
                                "id": "ada425db-1181-41af-a425-db118111aff9",
                                "email": "user@example.com",
                            },
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Validation Error",
                examples=[
                    OpenApiExample(
                        "Password Mismatch",
                        value={"password": ["Passwords do not match"]},
                    ),
                    OpenApiExample(
                        "Invalid Email", value={"email": ["Invalid email format"]}
                    ),
                ],
            ),
        },
        methods=["POST"],
        description="User registration endpoint",
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        tags=["auth"],
        request=OpenApiRequest(
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
        ),
        responses={
            200: OpenApiResponse(
                response=LoginSerializer,
                description="Successfully logged in",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "user": {
                                "id": "ada425db-1181-41af-a425-db118111aff9",
                                "email": "user@example.com",
                            },
                        },
                    )
                ],
            ),
        },
        methods=["POST"],
        description="User login endpoint",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    @extend_schema(
        tags=["auth"],
        request=OpenApiRequest(
            request=RefreshTokenSerializer,
            examples=[
                OpenApiExample(
                    "Refresh token example",
                    value={
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    },
                )
            ],
        ),
        responses={
            200: OpenApiResponse(
                response=RefreshTokenSerializer,
                description="Successfully refreshed token",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "user": {
                                "id": "ada425db-1181-41af-a425-db118111aff9",
                                "email": "user@example.com",
                            },
                        },
                    )
                ],
            ),
        },
        methods=["POST"],
        description="User refresh endpoint",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
