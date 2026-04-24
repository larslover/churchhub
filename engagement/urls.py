from django.urls import path
from . import views

app_name = "engagement"

urlpatterns = [
  path(
    "group/<int:group_id>/leader/",
    views.leader_dashboard,
    name="leader_dashboard"
),
    # -----------------------------------
    # Group Lists
    # -----------------------------------
    path("", views.group_list, name="group_list"),
    path("my/", views.my_groups, name="my_groups"),
    path("group/<int:group_id>/leader/remove/<int:user_id>/", views.remove_member, name="remove_member"),
path("post/<int:post_id>/pin/", views.toggle_pin_post, name="toggle_pin_post"),
path("invite/<int:invite_id>/leader/", views.leader_respond_invite, name="leader_respond_invite"),
path("group/<int:group_id>/meeting/create/", views.create_meeting, name="create_meeting"),

    # -----------------------------------
    # Group Actions
    # -----------------------------------
    path("<int:group_id>/", views.group_detail, name="group_detail"),
    path("<int:group_id>/join/", views.join_group, name="join_group"),
    path("<int:group_id>/leave/", views.leave_group, name="leave_group"),
    path("<int:group_id>/feed/", views.group_detail, name="group_feed"),

    # -----------------------------------
    # Invitations
    # -----------------------------------
    path(
        "group/<int:group_id>/invite/",
        views.invite_members,
        name="invite_members",
    ),

    path(
        "invite/<int:invite_id>/respond/",
        views.respond_invite,
        name="respond_invite",
    ),

    # -----------------------------------
    # Posts / Replies / Likes
    # -----------------------------------
    path(
        "post/<int:post_id>/delete/",
        views.delete_post,
        name="delete_post",
    ),

    path(
        "reply/<int:reply_id>/delete/",
        views.delete_reply,
        name="delete_reply",
    ),

    path(
        "post/<int:post_id>/like/",
        views.toggle_like,
        name="toggle_like",
    ),
  
    path("meeting/<int:meeting_id>/edit/", views.edit_meeting, name="edit_meeting"),
]