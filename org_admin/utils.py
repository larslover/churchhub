from accounts.models import (
    Organization,
    OrganizationMember,
    OrganizationJoinRequest,
)
from accounts.models import OrganizationMember

def get_admin_org(request):
    if not request.user.is_authenticated:
        return None

    membership = OrganizationMember.objects.filter(
        user=request.user,
        is_admin=True,
        is_active=True
    ).select_related("organization").first()

    if membership:
        return membership.organization

    return None