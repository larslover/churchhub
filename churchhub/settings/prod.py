# churchhub/settings/prod.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "kingdomlightchurch.co.za",
    "www.kingdomlightchurch.co.za",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "LarsLover$churchhub_prod",
        "USER": "LarsLover",
        "PASSWORD": "Lars1978",
        "HOST": "larslover.mysql.pythonanywhere-services.com",
        "PORT": "3306",
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True