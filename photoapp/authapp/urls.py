from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    UserInvitationView,
    UsersListView,
    UserRetrieveUpdateDestroyView,
    UserCreatePasswordView,
    UserCancelInvitationView,
    UserDeactivateView,
    UsersActiveListView,
)

app_name = 'authapp'

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token-verify'),
    path('user_invite/', UserInvitationView.as_view(), name='user-invite'),
    path('user_password_create/', UserCreatePasswordView.as_view(), name='user-password-create'),
    path('user_cancel_invitation/', UserCancelInvitationView.as_view(), name='user-cancel-invitation'),
    path('user_deactivate/', UserDeactivateView.as_view(), name='user-deactivate'),
    path('users/', UsersListView.as_view(), name='users'),
    path('active_users/', UsersActiveListView.as_view(), name='active-users'),
    path('users/<uuid:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-details'),
]
