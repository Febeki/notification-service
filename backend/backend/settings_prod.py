from .settings import *
from .settings import REST_FRAMEWORK, USE_HTTPS

CORS_ALLOWED_ORIGINS = [
    "http://domain.com",
    "http://*.domain.com",
]

X_FRAME_OPTIONS = "DENY"


if USE_HTTPS:
    CORS_ALLOWED_ORIGINS += [
        "https://domain.com",
        "https://*.domain.com",
    ]

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # a year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "strict-origin"
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True
