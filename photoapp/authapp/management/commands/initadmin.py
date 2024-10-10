from typing import Any
from django.core.management import BaseCommand
from django.contrib.auth.models import User
import logging

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        if User.objects.count() == 0:
            User.objects.create_superuser(
                username='admin',
                password='admin',
                email='testemail@mail.com',
            )
            log.info('Creating account for admin')
        else:
            log.info(
                'Admin accounts can only be initialized if no Accounts exist'
            )
