from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    UserRegisterView,
    UsersListView,
    UserRetrieveUpdateDestroyView,
)

app_name = "photoapp_api"

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('user_register/', UserRegisterView.as_view(), name='user_register'),
    path('users/', UsersListView.as_view(), name='users'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user_details'),
    # path('workday/start/', ..., name='workday_start_form'),
    # path('workday/end/', ..., name='workday_end_form'),
    # path('workday/stats/', ..., name='workday_stats'),
    # path('photo/upload/', ..., name='photo_upload_edit_qrcode'),
]
