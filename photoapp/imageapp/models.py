from django.db import models
import uuid
from authapp.models import User
from workdayapp.models import Restaurant


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(upload_to='photos/')
    qrcode = models.ImageField(upload_to='qrcode/')
    photo_in_frame = models.ImageField(upload_to='photo_in_frame/')
    photo_in_frame_with_qr_code = models.ImageField(upload_to='photo_in_frame_with_qr_code/')
    upload_time = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.photo.name


class Frame(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frame = models.ImageField(upload_to='frames/')
    upload_time = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='frames')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='frames')

    def __str__(self):
        return self.frame.name
