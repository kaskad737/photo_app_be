from django.urls import path
from .views import UploadPhotoView, DownloadPhotoView

app_name = 'imageapp'

urlpatterns = [
    path('upload/', UploadPhotoView.as_view(), name='upload-photo'),  # Эндпоинт для загрузки фотографии
    path('download/<int:pk>/', DownloadPhotoView.as_view(), name='download-photo'),  # Эндпоинт для скачивания
]
