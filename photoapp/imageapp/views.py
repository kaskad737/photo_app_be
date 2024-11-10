import os
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Photo, Frame
from .serializers import PhotoSerializer, FrameSerializer
from .utils import insert_photo_to_frame, create_qr_code, add_qr_code_to_image
from rest_framework.reverse import reverse
from django.http import HttpResponse


class UploadPhotoView(APIView):
    def post(self, request, *args, **kwargs):
        frame_id = self.request.data.get('frame_id')
        frame_instance = Frame.objects.filter(id=frame_id).first()

        qs_serializer = PhotoSerializer(
            data={
                'photo': request.FILES.get('file'),
                'uploaded_by': self.request.user.id
            },
            context={'request': request}
        )

        if qs_serializer.is_valid() and frame_instance:
            photo_instance = qs_serializer.save()
            download_url = reverse('imageapp:download-photo', args=[photo_instance.id])
            absolute_download_url = request.build_absolute_uri(download_url)

            # insert photo to our frame
            insert_photo_to_frame(
                photo_instance=photo_instance,
                frame_path=frame_instance.frame
            )

            # create qr code for our frame and photo
            create_qr_code(
                photo_instance=photo_instance,
                absolute_download_url=absolute_download_url
            )

            # add qr code to our frame and photo
            photo_in_frame_with_qr_code_bytes = add_qr_code_to_image(
                photo_instance=photo_instance
            )

            return HttpResponse(photo_in_frame_with_qr_code_bytes, content_type="image/png")

            # return Response(
            #     {
            #         'message': 'Media uploaded successfully.',
            #         'data': qs_serializer.data,
            #     },
            #     status=status.HTTP_200_OK,
            # )

        else:
            return Response(
                {'message': qs_serializer.errors, 'data': None},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DownloadPhotoView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            photo = Photo.objects.get(pk=pk)
            file_path = os.path.join(settings.MEDIA_ROOT, photo.photo_in_frame.name)
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            return Response({"detail": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
        except Photo.DoesNotExist:
            return Response({"detail": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)


class UploadFrameView(APIView):
    def post(self, request, *args, **kwargs):
        frame_serializer = FrameSerializer(
            data={
                'frame': request.FILES.get('file'),
                'uploaded_by': self.request.user.id
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
