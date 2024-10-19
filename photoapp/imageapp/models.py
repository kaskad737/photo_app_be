from django.db import models
import uuid


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(upload_to='photos/')
    qrcode = models.ImageField(upload_to='qrcode/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.photo.name


class Frame(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frame = models.ImageField(upload_to='frames/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.frame.name
