# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import ShiftStart, ShiftEnd
# from django.db.models import Q


@shared_task
def close_unfinished_shifts():
    now = timezone.now()
    today = now.date()
    end_of_day = timezone.datetime.combine(today, timezone.time(hour=23, minute=59))

    # Find all started but not closed shifts for today
    open_shifts = ShiftStart.objects.filter(
        timestamp__date=today
    ).exclude(
        id__in=ShiftEnd.objects.filter(timestamp__date=today).values_list('id', flat=True)
    )

    for shift in open_shifts:
        ShiftEnd.objects.create(
            restaurant=shift.restaurant,
            photographer=shift.photographer,
            frames_sold=0,  # Fill with zeros or other default logic
            photos_printed_4x6=0,
            postcards_printed=0,
            media_sets_used=0,
            cash_revenue=0.00,
            frames_given=0,
            frames_damaged=0,
            discount_approved=0.00,
            timestamp=end_of_day
        )
