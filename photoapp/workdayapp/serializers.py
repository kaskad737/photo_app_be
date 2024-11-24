from rest_framework import serializers
from .models import ShiftStart, ShiftEnd


class ShiftStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftStart
        fields = [
            'restaurant',
            'photographer',
            'frame_count',
            'media_set_count',
            'printer_life',
            'cash_in_envelope',
            'timestamp'
        ]
        read_only_fields = ['timestamp']


class ShiftEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftEnd
        fields = [
            'restaurant',
            'photographer',
            'frames_sold',
            'photos_printed_4x6',
            'postcards_printed',
            'media_sets_used',
            'cash_revenue',
            'frames_given',
            'frames_damaged',
            'discount_approved',
            'timestamp'
        ]
        read_only_fields = ['timestamp']
