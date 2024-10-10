from django.db import models


class Photo(models.Model):
    photo = models.ImageField(upload_to='photos/')  # Фотография сохраняется в директорию 'photos'
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)  # QR-код будет сохраняться в 'qrcodes'
    upload_time = models.DateTimeField(auto_now_add=True)  # Время загрузки
    download_url = models.URLField(max_length=200, null=True, blank=True)  # Ссылка на скачивание

    def __str__(self):
        return self.photo.name
