import os

from django.utils.translation import gettext_lazy as _

from .additional_settings.defender_settings import *
from .additional_settings.swagger_settings import *
from .additional_settings.cacheops_settings import *
from .additional_settings.logging_settings import *
from .additional_settings.celery_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = int(os.environ.get('DEBUG', 1))

ALLOWED_HOSTS: list = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

AUTH_USER_MODEL = 'main.User'

SUPERUSER_EMAIL = os.environ.get('SUPERUSER_EMAIL', 'test@test.com')
SUPERUSER_PASSWORD = os.environ.get('SUPERUSER_PASSWORD', 'tester26')

MICROSERVICE_TITLE = os.environ.get('MICROSERVICE_TITLE', 'Template')
MICROSERVICE_PREFIX = os.environ.get('MICROSERVICE_PREFIX', '')

REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379')

USE_HTTPS = int(os.environ.get('USE_HTTPS', 0))
ENABLE_SENTRY = int(os.environ.get('ENABLE_SENTRY', 0))
ENABLE_SILK = int(os.environ.get('ENABLE_SILK', 0))
ENABLE_DEBUG_TOOLBAR = int(os.environ.get('ENABLE_DEBUG_TOOLBAR', 0))
ENABLE_RENDERING = int(os.environ.get('ENABLE_RENDERING', 0))

INTERNAL_IPS = []

ADMIN_URL = os.environ.get('ADMIN_URL', 'admin')

SWAGGER_URL = os.environ.get('SWAGGER_URL')

API_KEY_HEADER = os.environ.get('API_KEY_HEADER')
API_KEY = os.environ.get('API_KEY')

HEALTH_CHECK_URL = os.environ.get('HEALTH_CHECK_URL', '/application/health/')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'defender',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'rosetta',
]

LOCAL_APPS = [
    'main.apps.MainConfig',
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'main.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'defender.middleware.FailedLoginMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('microservice_request.permissions.HasApiKeyOrIsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

if ENABLE_RENDERING:
    """For build CMS using DRF"""
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    )

ROOT_URLCONF = 'src.urls'

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'
ASGI_APPLICATION = 'src.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'CONN_MAX_AGE': 0,
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_SOCKET', 'unix:///redis_socket/redis-server.sock?db=1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TZ', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIMEZONE_COOKIE_NAME = 'timezone'
TIMEZONE_COOKIE_AGE = 15552000  # 60*60*24*180

STATIC_URL = f'{MICROSERVICE_PREFIX}/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = f'{MICROSERVICE_PREFIX}/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

LANGUAGES = (('en', _('English')),)

SESSION_COOKIE_NAME = 'sessionid'
CSRF_COOKIE_NAME = 'csrftoken'

if DEBUG:
    ROSETTA_SHOW_AT_ADMIN_PANEL = True


if JAEGER_AGENT_HOST := os.environ.get('JAEGER_AGENT_HOST'):
    from jaeger_client import Config
    from jaeger_client.config import DEFAULT_REPORTING_PORT
    from django_opentracing import DjangoTracing

    """If you don't need to trace all requests, comment middleware and set OPENTRACING_TRACE_ALL = False
        More information https://github.com/opentracing-contrib/python-django/#tracing-individual-requests
    """
    MIDDLEWARE.insert(0, 'django_opentracing.OpenTracingMiddleware')
    OPENTRACING_TRACE_ALL = True
    tracer = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'local_agent': {
                'reporting_port': os.environ.get('JAEGER_AGENT_PORT', DEFAULT_REPORTING_PORT),
                'reporting_host': JAEGER_AGENT_HOST,
            },
            'logging': int(os.environ.get('JAEGER_LOGGING', False)),
        },
        service_name=MICROSERVICE_TITLE,
        validate=True,
    ).initialize_tracer()
    OPENTRACING_TRACING = DjangoTracing(tracer)

if (SENTRY_DSN := os.environ.get('SENTRY_DSN')) and ENABLE_SENTRY:
    # More information on site https://sentry.io/
    from sentry_sdk import init
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            RedisIntegration(),
            CeleryIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '1.0')),
        environment=os.environ.get('SENTRY_ENV', 'development'),
        sample_rate=float(os.environ.get('SENTRY_SAMPLE_RATE', '1.0')),
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
