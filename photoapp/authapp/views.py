from authapp.models import User
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UsersListSerializer,
    UserSerializer,
)


@extend_schema_view(
    post=extend_schema(
        tags=['token'],
        summary='Get JWT Token',
        responses={
            status.HTTP_200_OK: {
                'type': 'object',
                'properties': {
                    'refresh': {'type': 'string'},
                    'access': {'type': 'string'},
                },
            },
        },
    ),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    post=extend_schema(
        tags=['token'],
        summary='Get JWT Token pair',
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


@extend_schema_view(
    post=extend_schema(
        tags=['token'],
        summary='Verify JWT Token',
    ),
)
class CustomTokenVerifyView(TokenVerifyView):
    permission_classes = [AllowAny]


@extend_schema_view(
    post=extend_schema(
        tags=['user_registration'],
        summary='User registration',
    ),
)
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    get=extend_schema(
        tags=['user'],
        summary='List all users',
    ),
)
class UsersListView(ListAPIView):
    serializer_class = UsersListSerializer
    queryset = User.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema_view(
    get=extend_schema(
        tags=['user'],
        summary='Get user instance',
    ),
    put=extend_schema(
        tags=['user'],
        summary='Change user instance',
    ),
    patch=extend_schema(
        tags=['user'],
        summary='Patch user instance',
    ),
    delete=extend_schema(
        tags=['user'],
        summary='Delete user instance',
    ),
)
class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsAdminUser]
