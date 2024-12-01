from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
                    },
                    'frame_count': {
                        'type': 'integer',
                        'description': 'Initial count of frames available (optional).',
                        'nullable': True
                    },
                    'media_set_count': {
                        'type': 'integer',
                        'description': 'Initial count of media sets available (optional).',
                        'nullable': True
                    },
                    'printer_life': {
                        'type': 'string',
                        'description': 'Printer life status (optional).',
                        'nullable': True
                    },
                    'cash_in_envelope': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Cash available in the envelope at the start of the shift (optional).',
                        'nullable': True
                    },
                    'timestamp': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'Timestamp indicating the start time of the shift.'
                    }
                },
                'required': ['photographer', 'restaurant', 'timestamp']
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
                        'frame_count': 50,
                        'media_set_count': 20,
                        'printer_life': 'Good',
                        'cash_in_envelope': 200.0,
                        'timestamp': '2024-11-21T08:00:00Z'
                    }
                }
            },
            400: {
                'description': 'Error in starting the shift.',
                'examples': {
                    'application/json': {
                        "photographer": ["This field is required."],
                        "restaurant": ["This field is required."],
                        "cash_in_envelope": ["Invalid value."]
                    }
                }
            }
        }
    ),
)
class ShiftStartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        photographer_id = request.data.get('photographer')
        restaurant_id = request.data.get('restaurant')
        today = timezone.now().date()

        if ShiftStart.objects.filter(
            photographer=photographer_id,
            restaurant=restaurant_id,
            timestamp__date=today
        ).exists():
            return Response(
                {"error": "Shift has already been started for this photographer and restaurant today."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ShiftStartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
                    },
                    'frames_sold': {
                        'type': 'integer',
                        'description': 'Number of frames sold during the shift.'
                    },
                    'photos_printed_4x6': {
                        'type': 'integer',
                        'description': 'Number of 4x6 photos printed during the shift.'
                    },
                    'postcards_printed': {
                        'type': 'integer',
                        'description': 'Number of postcards printed during the shift.'
                    },
                    'media_sets_used': {
                        'type': 'integer',
                        'description': 'Number of media sets used during the shift.'
                    },
                    'cash_revenue': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Total cash revenue collected during the shift.'
                    },
                    'frames_given': {
                        'type': 'integer',
                        'description': 'Number of frames given during the shift.'
                    },
                    'frames_damaged': {
                        'type': 'integer',
                        'description': 'Number of frames damaged during the shift.'
                    },
                    'discount_approved': {
                        'type': 'boolean',
                        'description': 'Whether any discounts were approved during the shift.'
                    },
                    'timestamp': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'Timestamp marking the end of the shift (provided by the frontend).'
                    },
                },
                'required': ['photographer', 'restaurant', 'timestamp']
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
                        'frames_sold': 30,
                        'photos_printed_4x6': 100,
                        'postcards_printed': 50,
                        'media_sets_used': 20,
                        'cash_revenue': 500.0,
                        'frames_given': 5,
                        'frames_damaged': 2,
                        'discount_approved': True,
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExcelReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Пример данных
        data = [
            ["10:00 AM", "6:00 PM", "8:00", 100, 50, 500, 200, 700],
            ["9:00 AM", "5:00 PM", "8:00", 120, 40, 600, 300, 900],
        ]
        return generate_excel_report(data)


class RestaurantCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
