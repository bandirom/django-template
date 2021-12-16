from .settings import INSTALLED_APPS, MIDDLEWARE, ENABLE_SILK, INTERNAL_IPS
from .settings import *

CORS_ORIGIN_ALLOW_ALL = True

if ENABLE_SILK:
    INSTALLED_APPS += ['silk']
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

if ENABLE_DEBUG_TOOLBAR:
    from socket import gethostbyname_ex, gethostname

    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    hostname, d, ips = gethostbyname_ex(gethostname())
    INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]
    # More info: https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-panels
    DEBUG_TOOLBAR_PANELS = [
        'ddt_request_history.panels.request_history.RequestHistoryPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
    DEBUG_TOOLBAR_CONFIG = {'RESULTS_CACHE_SIZE': 100}
