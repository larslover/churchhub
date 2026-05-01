from .models import OrganizationMember

from accounts.models import OrganizationMember

def org_admin_status(request):
    if not request.user.is_authenticated:
        return {"user_is_org_admin": False}

    return {
        "user_is_org_admin": OrganizationMember.objects.filter(
            user=request.user,
            is_admin=True,
            is_active=True
        ).exists()
    }
from accounts.models import OrganizationMember
def active_organization(request):
    if not request.user.is_authenticated:
        return {}

    membership = OrganizationMember.objects.filter(
        user=request.user
    ).select_related("organization").first()

    return {
        "active_organization": membership.organization if membership else None
    }