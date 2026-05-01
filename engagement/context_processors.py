from django.utils import timezone
from .models import GroupMember, Meeting
from org_admin.utils import get_admin_org
from .models import GroupMember,GroupInvitation

def user_groups(request):
    if request.user.is_authenticated:
        groups = GroupMember.objects.filter(
            user=request.user,
            is_active=True,
            group__is_active=True
        ).select_related("group")

        return {"user_groups": [membership.group for membership in groups]}

    return {"user_groups": []}
def next_meeting(request):
    if not request.user.is_authenticated:
        return {}

    org = get_admin_org(request)
    if not org:
        return {}

    meeting = Meeting.objects.filter(
        group__organization=org,
        group__members__user=request.user,
        group__members__is_active=True,
        start_time__gte=timezone.now()
    ).select_related("group").order_by("start_time").first()

    return {
        "next_group_meeting": meeting
    }


def user_groups(request):
    if request.user.is_authenticated:
        groups = GroupMember.objects.filter(
            user=request.user,
            is_active=True
        ).select_related("group")
        return {"user_groups": [gm.group for gm in groups]}
    return {}
def pending_invitations(request):
    if not request.user.is_authenticated:
        return {}

    org = get_admin_org(request)
    if not org:
        return {
            "pending_invites": [],
            "pending_invites_count": 0
        }

    invites = GroupInvitation.objects.filter(
        invited_user=request.user,
        accepted=False,
        group__organization=org
    ).select_related("group")

    return {
        "pending_invites": invites,
        "pending_invites_count": invites.count()
    }