# churchhub/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # include content URLs under /content/
    path("content/", include("content.urls")),

    # optionally set home page at root /
    path("", include("content.urls")),  # if home() is in content.urls with path ""
]