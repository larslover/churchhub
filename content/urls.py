from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("teachings/", views.teaching_list, name="teaching_list"),
    path("teaching/<int:pk>/", views.teaching_detail, name="teaching_detail"),

    path("topics/", views.topic_list, name="topic_list"),
    path("topics/<int:pk>/", views.topic_detail, name="topic_detail"),

    path("series/", views.series_list, name="series_list"),
    path(
    "books/",
    views.biblebook_list,
    name="biblebook_list",
),

path(
    "books/<int:pk>/",
    views.biblebook_detail,
    name="biblebook_detail",
),
    path(
        "churches/",
        views.church_list,
        name="church_list"
    ),
    path(
    "churches/<int:pk>/",
    views.church_detail,
    name="church_detail",
),
]