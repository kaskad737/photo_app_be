import os
import qrcode
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Photo, Frame
from .serializers import PhotoSerializer, FrameSerializer
from rest_framework.reverse import reverse
from django.core.files import File


class UploadPhotoView(APIView):
    def post(self, request, *args, **kwargs):
        qs_serializer = PhotoSerializer(
            data={
                'photo': request.FILES.get('file')
            },
            context={'request': request}
        )

        if qs_serializer.is_valid():
            photo_instance = qs_serializer.save()
            download_url = reverse('imageapp:download-photo', args=[photo_instance.id])
            absolute_download_url = request.build_absolute_uri(download_url)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(absolute_download_url)
            qr.make(fit=True)

            qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcode')
            if not os.path.exists(qr_dir):
                os.makedirs(qr_dir)

            qr_img = qr.make_image(fill='black', back_color='white')
            qr_path = os.path.join(qr_dir, f'{photo_instance.id}_qr.png')
            qr_img.save(qr_path)

            with open(qr_path, 'rb') as f:
                photo_instance.qrcode.save(f'{photo_instance.id}_qr.png', File(f))

            photo_instance.save()

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


class UploadFrameView(APIView):
    def post(self, request, *args, **kwargs):
        frame_serializer = FrameSerializer(
            data={
                'frame': request.FILES.get('file')
            },
            context={'request': request}
        )

        if frame_serializer.is_valid():
            frame_serializer.save()

            return Response(
                {
                    'message': 'Frame uploaded successfully.',
                    'data': frame_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {'message': frame_serializer.errors, 'data': None},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListFramesView(ListAPIView):
    serializer_class = FrameSerializer
    queryset = Frame.objects.all()
