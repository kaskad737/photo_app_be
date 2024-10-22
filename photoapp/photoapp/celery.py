import os
from celery import Celery

REDIS_HOST = os.getenv("REDIS_HOST")

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'photoapp.settings.base'
)

app = Celery(
    'photoapp',
    broker=f'redis://{REDIS_HOST}:6379/0',
    backend=f'redis://{REDIS_HOST}:6379/0',
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
