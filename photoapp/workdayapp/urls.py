from django.urls import path
from .views import ShiftStartAPIView, ShiftEndAPIView, ExcelReportView, RestaurantCreateView, RestaurantListView

app_name = 'workdayapp'

urlpatterns = [
    path('shift/start/', ShiftStartAPIView.as_view(), name='shift-start'),
    path('shift/end/', ShiftEndAPIView.as_view(), name='shift-end'),
    path("generate-report/", ExcelReportView.as_view(), name="generate-report"),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/register/', RestaurantCreateView.as_view(), name='restaurant-register'),
]
