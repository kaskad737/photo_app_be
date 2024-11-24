from django.urls import path
from .views import ShiftStartAPIView, ShiftEndAPIView

app_name = 'workdayapp'

urlpatterns = [
    path('shift/start/', ShiftStartAPIView.as_view(), name='shift-start'),
    path('shift/end/', ShiftEndAPIView.as_view(), name='shift-end'),
]
