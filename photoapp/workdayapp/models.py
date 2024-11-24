from django.db import models
from django.utils import timezone
from authapp.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ShiftStart(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restaurant")
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Photographer's Name")
    frame_count = models.PositiveIntegerField(verbose_name="Frame Count",
                                              help_text="Number of frames at the start of the shift")
    media_set_count = models.PositiveIntegerField(
        verbose_name="Media Set Count", help_text="Number of media sets at the start of the shift")
    printer_life = models.PositiveIntegerField(verbose_name="Printer Life", help_text="Printer life percentage")
    cash_in_envelope = models.DecimalField(max_digits=10, decimal_places=2,
                                           verbose_name="Cash in Envelope")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Date and Time",
                                     help_text="Automatically recorded date and time of the shift start")

    def __str__(self):
        return f"Shift Start: {self.restaurant.name} - {self.photographer.first_name} {self.photographer.last_name}"


class ShiftEnd(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name="Restaurant")
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Photographer's Name")
    frames_sold = models.PositiveIntegerField(verbose_name="Frames Sold")
    photos_printed_4x6 = models.PositiveIntegerField(verbose_name="Photos Printed 4x6")
    postcards_printed = models.PositiveIntegerField(verbose_name="Postcards Printed")
    media_sets_used = models.PositiveIntegerField(verbose_name="Media Sets Used")
    cash_revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cash Revenue")
    frames_given = models.PositiveIntegerField(verbose_name="Frames Given")
    frames_damaged = models.PositiveIntegerField(verbose_name="Frames Damaged")
    discount_approved = models.DecimalField(max_digits=10, decimal_places=2,
                                            verbose_name="Approved Discount Amount")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Date and Time",
                                     help_text="Automatically recorded date and time of the shift end")

    def __str__(self):
        return f"Shift End: {self.restaurant.name} - {self.photographer.first_name} {self.photographer.last_name}"
