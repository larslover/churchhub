# churchhub/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Include content URLs under /content/
    path("content/", include("content.urls")),

    # Set home page at root /
    path("", include("content.urls")),  # home() should be in content.urls with path ""
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)