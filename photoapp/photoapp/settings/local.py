from .base import *  # noqa
from datetime import timedelta

SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME': timedelta(days=365)}

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (  # noqa
    'rest_framework.authentication.SessionAuthentication',
)

LANGUAGE_CODE = 'en'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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


REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (  # noqa
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
)
