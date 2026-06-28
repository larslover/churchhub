from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Topics
    path("topics/", views.topic_list, name="topic_list"),
    path("topics/<int:pk>/", views.topic_detail, name="topic_detail"),

    # Series
    path("series/", views.series_list, name="series_list"),
    path("teaching/<int:pk>/", views.teaching_detail, name="teaching_detail"),
]