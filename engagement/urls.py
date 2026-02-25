from django.urls import path
from . import views

app_name = "engagement"

urlpatterns = [
    path("<int:group_id>/join/", views.join_group, name="join_group"),
    path("<int:group_id>/leave/", views.leave_group, name="leave_group"),
    path("<int:group_id>/", views.group_detail, name="group_detail"),
    path("", views.group_list, name="group_list"),
        path("group/<int:group_id>/invite/", views.invite_members, name="invite_members"),
        path(
    "invite/<int:invite_id>/respond/",
    views.respond_invite,
    name="respond_invite",
),
]
