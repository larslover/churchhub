# churchhub/settings/prod.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "wayoffaithglobal.com",
    "www.wayoffaithglobal.com",
    "webapp-2693333.pythonanywhere.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "LarsLover$churchhub",
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