from .settings import INSTALLED_APPS, MIDDLEWARE, ENABLE_SILK
from .settings import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if ENABLE_SILK:
    INSTALLED_APPS += ['silk']
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

CORS_ORIGIN_ALLOW_ALL = True
