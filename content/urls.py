from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("teachings/", views.teaching_list, name="teaching_list"),
    path("teaching/<int:pk>/", views.teaching_detail, name="teaching_detail"),

    path("topics/", views.topic_list, name="topic_list"),
    path("topics/<int:pk>/", views.topic_detail, name="topic_detail"),

    path("series/", views.series_list, name="series_list"),
]