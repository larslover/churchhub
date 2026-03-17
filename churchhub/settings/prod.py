# churchhub/settings/prod.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "klcapp.co.za",
    "www.klcapp.co.za",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "LarsLover$kingdomlightchurch",
        "USER": "LarsLover",
        "PASSWORD": "Lars1978",
        "HOST": "LarsLover.mysql.pythonanywhere-services.com",
        "PORT": "3306",
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True