# content/urls.py
from django.urls import path
from .views import home,devotional_archive  # only import what exists


urlpatterns = [
    path("", home, name="home"),
    path("devotionals/", devotional_archive, name="devotional_archive"),

]