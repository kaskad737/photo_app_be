from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from django.utils import timezone
from .models import ShiftStart, Restaurant
from .serializers import ShiftStartSerializer, ShiftEndSerializer, RestaurantSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from .utils import generate_excel_report


@extend_schema_view(
    post=extend_schema(
        tags=['workday'],
        summary='Start Shift',
        description='Marks the beginning of a work shift for a photographer at a specified restaurant.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'photographer': {
                        'type': 'integer',
                        'description': 'ID of the photographer starting the shift.'
                    },
                    'restaurant': {
                        'type': 'integer',
                        'description': 'ID of the restaurant where the shift is starting.'
                    }
                },
                'required': ['photographer', 'restaurant']
            }
        },
        responses={
            201: {
                'description': 'Shift started successfully.',
                'examples': {
                    'application/json': {
                        'id': 1,
                        'photographer': 10,
                        'restaurant': 5,
                        'timestamp': '2024-11-21T08:00:00Z'
                    }
                }
            },
            400: {
                'description': 'Error in starting the shift.',
                'examples': {
                    'application/json': {
                        "photographer": ["This field is required."],
                        "restaurant": ["This field is required."]
                    }
                }
            }
        }
    ),
)
class ShiftStartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ShiftStartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(timestamp=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        tags=['workday'],
        summary='End Shift',
        description='Marks the end of a work shift for a photographer at a specified restaurant. '
                    'This endpoint ensures that the shift was started earlier on the same day.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'photographer': {
                        'type': 'integer',
                        'description': 'ID of the photographer ending the shift.'
                    },
                    'restaurant': {
                        'type': 'integer',
                        'description': 'ID of the restaurant where the shift is ending.'
                    }
                },
                'required': ['photographer', 'restaurant']
            }
        },
        responses={
            201: {
                'description': 'Shift ended successfully.',
                'examples': {
                    'application/json': {
                        'id': 1,
                        'photographer': 10,
                        'restaurant': 5,
                        'timestamp': '2024-11-21T15:30:00Z'
                    }
                }
            },
            400: {
                'description': 'Error in ending the shift.',
                'examples': {
                    'application/json': {
                        "error": "You cannot close a shift without starting it that day."
                    }
                }
            }
        }
    ),
)
class ShiftEndAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        photographer = request.data.get('photographer')
        restaurant = request.data.get('restaurant')
        today = timezone.now().date()

        # Check to see if ShiftStart was started for this photographer and restaurant today
        if not ShiftStart.objects.filter(
            photographer=photographer,
            restaurant=restaurant,
            timestamp__date=today
        ).exists():
            return Response(
                {"error": "You cannot close a shift without starting it that day."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ShiftEndSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(timestamp=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExcelReportView(APIView):
    def get(self, request):
        # Пример данных
        data = [
            ["10:00 AM", "6:00 PM", "8:00", 100, 50, 500, 200, 700],
            ["9:00 AM", "5:00 PM", "8:00", 120, 40, 600, 300, 900],
        ]
        return generate_excel_report(data)


class RestaurantCreateView(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantRetrieveView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
