from datetime import timedelta

from .base import *  # noqa

SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(minutes=30)}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '%(asctime)s.%(msecs)03d | %(name)-25s | %(levelname)-9s | %(lineno)-4d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'base'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)  # noqa
