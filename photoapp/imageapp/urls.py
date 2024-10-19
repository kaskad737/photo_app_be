from django.urls import path
from .views import UploadPhotoView, DownloadPhotoView, UploadFrameView, ListFramesView

app_name = 'imageapp'

urlpatterns = [
    path('upload/', UploadPhotoView.as_view(), name='upload-photo'),
    path('download/<uuid:pk>/', DownloadPhotoView.as_view(), name='download-photo'),
    path('upload_frame/', UploadFrameView.as_view(), name='download-frame'),
    path('list_frames/', ListFramesView.as_view(), name='list-frames')
]
