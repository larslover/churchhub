from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, GroupMember



from .models import Group
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Group, GroupMember, GroupInvitation
from django.contrib.auth import get_user_model

User = get_user_model()
@login_required
def invite_members(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if group.leader != request.user:
        messages.error(request, "You are not the leader of this group.")
        return redirect("engagement:group_detail", group.id)

    query = request.GET.get("q", "").strip()

    eligible_users = User.objects.none()

    if query:
        # Exclude users already in any small group
        other_small_group_members = GroupMember.objects.filter(
            group__group_type="small"
        ).values_list("user_id", flat=True)

        eligible_users = (
            User.objects
            .exclude(id__in=other_small_group_members)
            .filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            .order_by("username")[:20]   # LIMIT results
        )

    if request.method == "POST":
        user_ids = request.POST.getlist("users")
        for uid in user_ids:
            user = User.objects.get(id=uid)
            GroupInvitation.objects.get_or_create(
                group=group,
                invited_user=user,
                invited_by=request.user
            )
        messages.success(request, "Invitations sent successfully!")
        return redirect("engagement:group_detail", group.id)

    return render(request, "engagement/invite_members.html", {
        "group": group,
        "eligible_users": eligible_users,
        "query": query,
    })

def group_list(request):
    groups = Group.objects.filter(is_active=True).select_related("leader")
    
    # Annotate each group with whether the current user is a member
    user_memberships = []
    if request.user.is_authenticated:
        user_memberships = GroupMember.objects.filter(
            user=request.user,
            is_active=True
        ).values_list('group_id', flat=True)

    for group in groups:
        group.is_member = group.id in user_memberships
        group.member_count = group.members.filter(is_active=True).count()

    return render(request, "engagement/group_list.html", {"groups": groups})
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    is_member = False
    if request.user.is_authenticated:
        is_member = GroupMember.objects.filter(
            user=request.user,
            group=group
        ).exists()

    context = {
        "group": group,
        "is_member": is_member,
    }

    return render(request, "engagement/group_detail.html", context)
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
        messages.info(request, "You are already a member of this group.")

    return redirect("engagement:group_detail", group_id=group.id)


@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    GroupMember.objects.filter(
        user=request.user,
        group=group
    ).delete()

    messages.success(request, f"You left {group.name}.")
    return redirect("engagement:group_detail", group_id=group.id)

@login_required
def respond_invite(request, invite_id):
    invitation = get_object_or_404(
        GroupInvitation,
        id=invite_id,
        invited_user=request.user
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "accept":
            # Create membership if not already a member
            GroupMember.objects.get_or_create(
                user=request.user,
                group=invitation.group
            )
            messages.success(request, f"You joined {invitation.group.name}.")

        elif action == "decline":
            messages.info(request, "Invitation declined.")

        # Delete invitation after response
        invitation.delete()

        return redirect("engagement:group_detail", group_id=invitation.group.id)

    return redirect("engagement:group_list")