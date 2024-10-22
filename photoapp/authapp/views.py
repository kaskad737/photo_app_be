from authapp.models import User
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
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
    UsersListSerializer,
    UserSerializer,
    InvitationSerializer,
    PasswordCheckAndSetSerializer,
    EmailSerializer,
)
from rest_framework.response import Response
from .utils import make_invitation_reset_link, data_unsigner, create_password
from .tasks import send_invite_email
from django.shortcuts import get_object_or_404


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


@extend_schema_view(
    post=extend_schema(
        tags=['user_actions'],
        summary='User invitation',
        request=InvitationSerializer,
        responses={
            200: "Invitation sent successfully.",
            400: "User with this email already exists or invalid data."
        },
    ),
)
class UserInvitationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
            created_user = User.objects.create(
                username=serializer.validated_data['email'],
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                is_invited=True
            )
            created_user.set_password('')
            created_user.save()
            invite_url = make_invitation_reset_link(user=created_user, type='invitation')
            send_invite_email(user_first_name=created_user.first_name, email=email, invite_url=invite_url)
            return Response({"message": "Invitation sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    put=extend_schema(
        tags=["user_actions"],
        request=PasswordCheckAndSetSerializer,
        responses={200: {"type": "object", "properties": {"user_pk": {"type": "string"}}}},
    ),
)
class UserCreatePasswordView(APIView):
    def put(self, request):
        serializer = PasswordCheckAndSetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            invitation_signed_token = self.request.data.get("invitation")
            password = self.request.data.get("password1")
            signature = data_unsigner(invitation_signed_token=invitation_signed_token)
            if signature:
                user = get_object_or_404(User, pk=signature.get("pk"))
                if user and user.is_invited:
                    create_password(user_to_update=user, password=password)
                    return Response(data={"pk": str(user.pk)}, status=status.HTTP_200_OK)
                elif not user.is_invited:
                    return Response({"message": "The invitation has been rescinded"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "The invitation has expired"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Signature does not match"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        tags=['user_actions'],
        summary='Cancel User Invitation',
        description='Cancel an existing user invitation before they have accepted or activated their account.',
        request=EmailSerializer,
        responses={
            200: "Invitation canceled successfully.",
            404: "User with this email not found.",
            400: "Invalid request, or user already activated.",
        },
    ),
)
class UserCancelInvitationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email, is_invited=True).first()
        if not user:
            return Response(
                {"error": "User not found or invitation already canceled/activated."},
                status=status.HTTP_404_NOT_FOUND
            )
        user.is_invited = False
        user.save()
        return Response({"message": "Invitation canceled successfully."}, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        tags=['user_actions'],
        summary='Deactivate User',
        description='Deactivate a user, preventing them from logging in.',
        request=EmailSerializer,
        responses={
            200: "User deactivated successfully.",
            404: "User with this email not found.",
            400: "Invalid request.",
        },
    ),
)
class UserDeactivateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.is_active = False
        user.save()
        return Response({"message": "User deactivated successfully."}, status=status.HTTP_200_OK)
