import os
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Photo, Frame
from .serializers import PhotoSerializer, FrameSerializer, ListPhotoSerializer, RetrievePhotoSerializer
from .utils import insert_photo_to_frame, create_qr_code, add_qr_code_to_image
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser


@extend_schema_view(
    post=extend_schema(
        tags=['image'],
        summary='Upload photo',
    ),
)
class UploadPhotoView(APIView):
    permission_classes = [IsAuthenticated]

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
            download_url = f'{settings.FE_HOST}/{settings.IMAGE_DOWNLOAD_PATH}/{photo_instance.id}'

            # insert photo to our frame
            insert_photo_to_frame(
                photo_instance=photo_instance,
                frame_path=frame_instance.frame
            )

            # create qr code for our frame and photo
            create_qr_code(
                photo_instance=photo_instance,
                absolute_download_url=download_url
            )

            # add qr code to our frame and photo
            photo_in_frame_with_qr_code_bytes = add_qr_code_to_image(
                photo_instance=photo_instance
            )

            return HttpResponse(photo_in_frame_with_qr_code_bytes, content_type="image/png")

        else:
            return Response(
                {'message': qs_serializer.errors, 'data': None},
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema_view(
    get=extend_schema(
        tags=['image'],
        summary='Download photo',
        responses={
            200: OpenApiResponse(
                response={"type": "string", "format": "binary"},
                description="A downloadable photo file."
            ),
            404: OpenApiResponse(
                response={"type": "string", "format": "binary"},
                description="Photo not found."
            ),
        },
    ),
)
class DownloadPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            photo = Photo.objects.get(pk=pk)
            file_path = os.path.join(settings.MEDIA_ROOT, photo.photo_in_frame.name)
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            return Response({"detail": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
        except Photo.DoesNotExist:
            return Response({"detail": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    post=extend_schema(
        tags=['image'],
        summary='Upload frame',
    ),
)
class UploadFrameView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        restaurant_id = self.request.data.get('restaurant')

        if Frame.objects.filter(restaurant_id=restaurant_id).exists():
            return Response(
                {
                    'message': '''
                        A frame for this restaurant already exists. You cannot upload a new one.
                        You can delete it and upload new or update it.
                    ''',
                    'data': None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        frame_serializer = FrameSerializer(
            data={
                'frame': request.FILES.get('file'),
                'uploaded_by': self.request.user.id,
                'restaurant': restaurant_id
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


@extend_schema_view(
    get=extend_schema(
        tags=['image'],
        summary='List frames',
    ),
)
class ListFramesView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = FrameSerializer
    queryset = Frame.objects.all()


@extend_schema_view(
    get=extend_schema(
        tags=['image'],
        summary='List photos',
    ),
)
class ListPhotosView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListPhotoSerializer
    queryset = Photo.objects.all()


@extend_schema_view(
    get=extend_schema(
        tags=['image'],
        summary='Retrieve photo',
    ),
)
class RetrievePhotoView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetrievePhotoSerializer
    queryset = Photo.objects.all()
