from .settings import INSTALLED_APPS, MIDDLEWARE
from .settings import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += [
    # 'silk',
]

MIDDLEWARE += [
    # 'silk.middleware.SilkyMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:8000',
#     'http://localhost:3000',
# ]
