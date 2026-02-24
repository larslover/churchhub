# churchhub/settings/prod.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = ["yourchurchdomain.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "churchhub_prod",
        "USER": "dbuser",
        "PASSWORD": "securepassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True