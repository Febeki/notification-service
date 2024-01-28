from .settings import *
from .settings import INSTALLED_APPS, INTERNAL_IPS, MIDDLEWARE

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True

if ENABLE_DEBUG_TOOLBAR:
    from socket import gethostbyname_ex, gethostname

    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    hostname, d, ips = gethostbyname_ex(gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]