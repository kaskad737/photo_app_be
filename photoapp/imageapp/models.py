from django.db import models


class Photo(models.Model):
    photo = models.ImageField(upload_to='photos/')  # Фотография сохраняется в директорию 'photos'
    upload_time = models.DateTimeField(auto_now_add=True)  # Время загрузки

    def __str__(self):
        return self.photo.name
