from .models import OrganizationMember

def org_admin_status(request):
    org_id = request.session.get("organization_id")

    if request.user.is_authenticated and org_id:
        is_admin = OrganizationMember.objects.filter(
            user=request.user,
            organization_id=org_id,
            is_admin=True
        ).exists()

        return {"user_is_org_admin": is_admin}

    return {"user_is_org_admin": False}

from accounts.models import OrganizationMember

def active_organization(request):
    if not request.user.is_authenticated:
        return {}

    membership = OrganizationMember.objects.filter(
        user=request.user,
        is_active=True
    ).select_related("organization").first()

    if not membership:
        return {
            "active_organization": None
        }

    return {
        "active_organization": membership.organization
    }