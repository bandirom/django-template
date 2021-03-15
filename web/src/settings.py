import os

from django.utils.translation import gettext_lazy as _

from .additional_settings.defender_settings import *
from .additional_settings.swagger_settings import *
from .additional_settings.cacheops_settings import *
from .additional_settings.logging_settings import *
from .additional_settings.celery_settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", default=1))

ALLOWED_HOSTS: list = os.environ.get("DJANGO_ALLOWED_HOSTS").split(",")

AUTH_USER_MODEL = 'main.User'

SUPERUSER_EMAIL = os.environ.get('SUPERUSER_EMAIL', 'test@test.com')
SUPERUSER_PASSWORD = os.environ.get('SUPERUSER_PASSWORD', 'tester26')

MICROSERVICE_TITLE = os.environ.get('MICROSERVICE_TITLE', 'Template')

REDIS_URL = os.environ.get('REDIS_URL')

USE_HTTPS = int(os.environ.get('USE_HTTPS', 0))
ENABLE_SILK = int(os.environ.get('ENABLE_SILK', 0))
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin')

SWAGGER_URL = os.environ.get('SWAGGER_URL')

API_KEY_HEADER = os.environ.get('API_KEY_HEADER')
API_KEY = os.environ.get('API_KEY')

INSTALLED_APPS = [
    'main.apps.MainConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'defender',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'rosetta',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
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
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

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
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
        "CONN_MAX_AGE": 0,
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('en', _('English')),
)

ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = LANGUAGE_CODE
ROSETTA_MESSAGES_SOURCE_LANGUAGE_NAME = 'English'
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
