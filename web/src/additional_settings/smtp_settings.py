from os import environ

EMAIL_HOST = environ.get("EMAIL_HOST")
EMAIL_PORT = int(environ.get("EMAIL_PORT", 465))
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = environ.get("DEFAULT_FROM_EMAIL")
EMAIL_TIMEOUT = int(environ.get("EMAIL_TIMEOUT", 15))
EMAIL_USE_SSL = int(environ.get("EMAIL_USE_SSL", 0))
EMAIL_USE_TLS = int(environ.get("EMAIL_USE_TLS", 0))
