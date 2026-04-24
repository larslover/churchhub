from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime

from .models import (
    Group,
    GroupMember,
    GroupInvitation,
    GroupPost,
    PostReply,
    PostLike,
    Meeting,
)

User = get_user_model()


# =========================
# 🔐 HELPERS
# =========================
def is_leader(user, group):
    return group.leader_id == user.id


# =========================
# 👑 LEADER DASHBOARD
# =========================
from .models import Meeting

@login_required
def leader_dashboard(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if group.leader != request.user:
        messages.error(request, "You are not the leader of this group.")
        return redirect("engagement:group_detail", group_id=group.id)

    members = GroupMember.objects.filter(
        group=group,
        is_active=True
    ).select_related("user")

    pending_invites = GroupInvitation.objects.filter(
        group=group,
        accepted=False
    )

    meetings = Meeting.objects.filter(group=group).order_by("-start_time")

    return render(request, "engagement/leader_dashboard.html", {
        "group": group,
        "members": members,
        "pending_invites": pending_invites,
        "meetings": meetings,   # ✅ THIS FIXES IT
    })

# =========================
# 📌 GROUP LIST
# =========================
def group_list(request):
    groups = Group.objects.filter(is_active=True).select_related("leader")

    user_memberships = set()

    if request.user.is_authenticated:
        user_memberships = set(
            GroupMember.objects.filter(
                user=request.user,
                is_active=True
            ).values_list("group_id", flat=True)
        )

    for group in groups:
        group.is_member = group.id in user_memberships
        group.member_count = group.members.filter(is_active=True).count()

    return render(request, "engagement/group_list.html", {"groups": groups})


# =========================
# 👤 MY GROUPS
# =========================
@login_required
def my_groups(request):
    memberships = GroupMember.objects.filter(
        user=request.user,
        is_active=True
    ).select_related("group", "group__leader")

    groups = [m.group for m in memberships]

    for group in groups:
        group.member_count = group.members.filter(is_active=True).count()

    return render(request, "engagement/my_groups.html", {"groups": groups})


# =========================
# 📄 GROUP DETAIL
# =========================
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    is_member = GroupMember.objects.filter(
        user=request.user,
        group=group
    ).exists()

    if request.method == "POST" and is_member:

        post_content = request.POST.get("post_content", "").strip()
        if post_content:
            GroupPost.objects.create(
                group=group,
                author=request.user,
                content=post_content
            )
            messages.success(request, "Post created!")
            return redirect("engagement:group_detail", group_id=group.id)

        reply_content = request.POST.get("reply_content", "").strip()
        post_id = request.POST.get("post_id")

        if reply_content and post_id:
            post = get_object_or_404(GroupPost, id=post_id)

            PostReply.objects.create(
                post=post,
                author=request.user,
                content=reply_content
            )

            messages.success(request, "Reply added!")
            return redirect("engagement:group_detail", group_id=group.id)

    posts = GroupPost.objects.filter(
        group=group
    ).prefetch_related("replies", "likes", "author")

    return render(request, "engagement/group_detail.html", {
        "group": group,
        "is_member": is_member,
        "posts": posts,
    })


# =========================
# ➕ JOIN GROUP
# =========================
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    membership, created = GroupMember.objects.get_or_create(
        user=request.user,
        group=group
    )

    if created:
        messages.success(request, f"You joined {group.name}.")
    else:
        messages.info(request, "Already a member.")

    return redirect("engagement:group_detail", group_id=group.id)


# =========================
# 🚪 LEAVE GROUP
# =========================
@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    GroupMember.objects.filter(
        user=request.user,
        group=group
    ).delete()

    messages.success(request, f"You left {group.name}.")
    return redirect("engagement:my_groups")


# =========================
# ❤️ LIKE POST
# =========================
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(GroupPost, id=post_id)

    like = PostLike.objects.filter(post=post, user=request.user)

    if like.exists():
        like.delete()
    else:
        PostLike.objects.create(post=post, user=request.user)

    return redirect("engagement:group_detail", group_id=post.group.id)


# =========================
# 🗑 DELETE POST
# =========================
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(GroupPost, id=post_id, author=request.user)
    group_id = post.group.id

    post.delete()

    messages.success(request, "Post deleted.")
    return redirect("engagement:group_detail", group_id=group_id)


# =========================
# 🗑 DELETE REPLY
# =========================
@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(PostReply, id=reply_id, author=request.user)
    group_id = reply.post.group.id

    reply.delete()

    messages.success(request, "Reply deleted.")
    return redirect("engagement:group_detail", group_id=group_id)


# =========================
# 📩 INVITE MEMBERS
# =========================
@login_required
def invite_members(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if not is_leader(request.user, group):
        messages.error(request, "Only leader can invite.")
        return redirect("engagement:group_detail", group_id=group.id)

    query = request.GET.get("q", "").strip()
    eligible_users = User.objects.none()

    if query:
        existing_members = GroupMember.objects.filter(
            group=group
        ).values_list("user_id", flat=True)

        eligible_users = User.objects.exclude(
            id__in=existing_members
        ).filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query)
        )[:20]

    if request.method == "POST":
        for uid in request.POST.getlist("users"):
            user = User.objects.get(id=uid)

            GroupInvitation.objects.get_or_create(
                group=group,
                invited_user=user,
                invited_by=request.user
            )

        messages.success(request, "Invitations sent.")
        return redirect("engagement:group_detail", group_id=group.id)

    return render(request, "engagement/invite_members.html", {
        "group": group,
        "eligible_users": eligible_users,
        "query": query,
    })


# =========================
# 📩 RESPOND INVITE (MEMBER)
# =========================
@login_required
def respond_invite(request, invite_id):
    invite = get_object_or_404(
        GroupInvitation,
        id=invite_id,
        invited_user=request.user
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "accept":
            GroupMember.objects.get_or_create(
                user=request.user,
                group=invite.group
            )
            messages.success(request, "Invitation accepted.")
        else:
            messages.info(request, "Invitation declined.")

        group_id = invite.group.id
        invite.delete()

        return redirect("engagement:group_detail", group_id=group_id)

    return redirect("engagement:group_list")


# =========================
# ❌ REMOVE MEMBER (LEADER)
# =========================
@login_required
def remove_member(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)

    if not is_leader(request.user, group):
        messages.error(request, "Not allowed.")
        return redirect("engagement:group_detail", group_id=group.id)

    if group.leader_id == user_id:
        messages.error(request, "Cannot remove leader.")
        return redirect("engagement:leader_dashboard", group_id=group.id)

    GroupMember.objects.filter(group=group, user_id=user_id).delete()

    return redirect("engagement:leader_dashboard", group_id=group.id)


# =========================
# 📌 PIN / UNPIN POST
# =========================
@login_required
def toggle_pin_post(request, post_id):
    post = get_object_or_404(GroupPost, id=post_id)
    group = post.group

    if not is_leader(request.user, group):
        messages.error(request, "Only leader can pin posts.")
        return redirect("engagement:group_detail", group_id=group.id)

    post.is_pinned = not post.is_pinned
    post.save()

    return redirect("engagement:leader_dashboard", group_id=group.id)


# =========================
# 👑 LEADER INVITE RESPONSE
# =========================
@login_required
def leader_respond_invite(request, invite_id):
    invite = get_object_or_404(GroupInvitation, id=invite_id)
    group = invite.group

    if not is_leader(request.user, group):
        messages.error(request, "Not allowed.")
        return redirect("engagement:group_detail", group_id=group.id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "approve":
            GroupMember.objects.get_or_create(
                user=invite.invited_user,
                group=group
            )
            messages.success(request, "Member approved.")
        else:
            messages.info(request, "Invite rejected.")

        invite.delete()

    return redirect("engagement:leader_dashboard", group_id=group.id)


# =========================
# 📅 CREATE MEETING
# =========================
@login_required
def create_meeting(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if not is_leader(request.user, group):
        messages.error(request, "Only leader can create meetings.")
        return redirect("engagement:group_detail", group_id=group.id)

    if request.method == "POST":
        title = request.POST.get("title")
        start_time = parse_datetime(request.POST.get("start_time"))

        if title and start_time:
            Meeting.objects.create(
                group=group,
                title=title,
                start_time=start_time
            )
            messages.success(request, "Meeting created!")

    return redirect("engagement:leader_dashboard", group_id=group.id)
@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if group.leader != request.user:
        messages.error(request, "Only leader can edit group.")
        return redirect("engagement:group_detail", group_id=group.id)

    if request.method == "POST":
        group.name = request.POST.get("name")
        group.description = request.POST.get("description")

        if "image" in request.FILES:
            group.image = request.FILES["image"]

        group.save()
        messages.success(request, "Group updated successfully!")

        return redirect("engagement:leader_dashboard", group_id=group.id)

    return render(request, "engagement/edit_group.html", {"group": group})