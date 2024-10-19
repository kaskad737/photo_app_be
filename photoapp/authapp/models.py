from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class UserRole(models.TextChoices):
    PHOTOGRAPHER = 'photographer', 'Photographer'
    ADMIN = 'admin', 'Admin'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=15, choices=UserRole.choices, default=UserRole.PHOTOGRAPHER)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
