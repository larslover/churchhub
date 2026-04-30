from accounts.models import (
    Organization,
    OrganizationMember,
    OrganizationJoinRequest,
)

def get_admin_org(request):
    org_id = request.session.get("organization_id")

    membership = OrganizationMember.objects.filter(
        user=request.user,
        organization_id=org_id,
        is_admin=True,
        is_active=True
    ).select_related("organization").first()

    if membership:
        return membership.organization

    return None