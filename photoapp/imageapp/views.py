import os
import qrcode
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Photo
from .serializers import PhotoSerializer
from django.urls import reverse


class UploadPhotoView(APIView):
    def post(self, request, *args, **kwargs):
        # Сериализация данных
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем фото
            photo_instance = serializer.save()

            # Генерация URL для скачивания фото
            download_url = request.build_absolute_uri(reverse('download-photo', args=[photo_instance.id]))
            photo_instance.download_url = download_url

            # Генерация QR-кода для этого URL
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(download_url)
            qr.make(fit=True)

            # Сохранение QR-кода на диск
            qr_img = qr.make_image(fill='black', back_color='white')
            qr_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', f'{photo_instance.id}_qr.png')
            qr_img.save(qr_path)

            # Сохраняем путь к QR-коду в базе данных
            photo_instance.qr_code = f'qrcodes/{photo_instance.id}_qr.png'
            photo_instance.save()

            return Response(PhotoSerializer(photo_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
