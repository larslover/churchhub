# churchhub/settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
AUTH_USER_MODEL = "accounts.User"
SECRET_KEY = "replace-this-in-prod"
# churchhub/healthapp/settings/base.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # your apps
    "accounts",
    "groups",
    "content",
    "giving",
    "engagement",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "churchhub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "engagement.context_processors.next_meeting",
             "engagement.context_processors.user_groups",
            "django.contrib.messages.context_processors.messages",
              "content.context_processors.global_updates",  # add this
              "engagement.context_processors.user_groups",
                "engagement.context_processors.pending_invitations",
        ]},
    },
]

WSGI_APPLICATION = "churchhub.wsgi.application"

AUTH_USER_MODEL = "accounts.User"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Johannesburg"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# Redirect after login/logout
LOGIN_REDIRECT_URL = "/"    # after login, go to home
LOGOUT_REDIRECT_URL = "/"   # after logout, go to home