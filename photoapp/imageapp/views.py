import os
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Photo
from .serializers import PhotoSerializer


class UploadPhotoView(APIView):
    def post(self, request, *args, **kwargs):
        qs_serializer = PhotoSerializer(
            data={
                'photo': request.FILES.get('file')
            },
            context={'request': request}
        )

        if qs_serializer.is_valid():
            qs_serializer.save()
            return Response(
                {
                    'message': 'Media uploaded successfully.',
                    'data': qs_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {'message': qs_serializer.errors, 'data': None},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DownloadPhotoView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            photo = Photo.objects.get(pk=pk)
            # Путь к файлу на диске
            file_path = os.path.join(settings.MEDIA_ROOT, photo.photo.name)
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            return Response({"detail": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
        except Photo.DoesNotExist:
            return Response({"detail": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
