# content/urls.py
from django.urls import path
from .views import home  # only import what exists

urlpatterns = [
    path("", home, name="home"),
]