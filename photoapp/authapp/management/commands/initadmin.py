from typing import Any
from django.core.management import BaseCommand
from authapp.models import User
import logging

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        if User.objects.count() == 0:
            User.objects.create_superuser(
                username='admin@mail.com',
                password='admin123',
                email='admin@mail.com',
                is_active=True,
            )
            log.info('Creating account for admin')
        else:
            log.info(
                'Admin accounts can only be initialized if no Accounts exist'
            )
