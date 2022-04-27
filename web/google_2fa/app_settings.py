from django.conf import settings
from urllib.parse import urljoin

from django.core.exceptions import ImproperlyConfigured

GOOGLE_2FA_API_KEY: str = getattr(settings, "GOOGLE_2FA_API_KEY", None)

if not GOOGLE_2FA_API_KEY:
    raise ImproperlyConfigured('Please, provide the api key for Google 2FA. In settings "GOOGLE_2FA_API_KEY"')

GOOGLE_2FA_URL: str = getattr(settings, "GOOGLE_2FA_URL", "https://google-authenticator.p.rapidapi.com")
GOOGLE_2FA_ISSUER: str = getattr(settings, "GOOGLE_2FA_ISSUER", "Example site")

GOOGLE_2FA_ENDPOINTS: dict = {
    "validate": urljoin(GOOGLE_2FA_URL, "validate/"),
    "new_v2": urljoin(GOOGLE_2FA_URL, "new_v2/"),
    "enroll": urljoin(GOOGLE_2FA_URL, "enroll/"),
}
