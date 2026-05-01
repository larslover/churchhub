from django.urls import path
from . import views
app_name = "org_admin"
urlpatterns = [
    path("dashboard/", views.org_dashboard_view, name="org_dashboard"),
    path("requests/", views.org_requests_view, name="org_requests"),
    path("requests/approve/<int:request_id>/", views.approve_org_request_view, name="approve_org_request"),
    path("devotionals/", views.devotional_list, name="devotional_list"),
path("updates/", views.update_list, name="update_list"),

path("programs/", views.program_list, name="program_list"),
path(
    "devotionals/new/",
    views.devotional_create,
    name="devotional_create"
),
path(
    "devotionals/<int:pk>/edit/",
    views.devotional_edit,
    name="devotional_edit"
),

path(
    "devotionals/<int:pk>/delete/",
    views.devotional_delete,
    name="devotional_delete"
),
path("updates/", views.update_list, name="update_list"),
path("updates/new/", views.update_create, name="update_create"),
path("updates/<int:pk>/edit/", views.update_edit, name="update_edit"),
path("updates/<int:pk>/delete/", views.update_delete, name="update_delete"),


path("media/", views.media_list, name="media_list"),
path("media/new/", views.media_create, name="media_create"),
path("media/<int:pk>/edit/", views.media_edit, name="media_edit"),
path("media/<int:pk>/delete/", views.media_delete, name="media_delete"),
]