from .models import OrganizationMember

def org_admin_status(request):
    if request.user.is_authenticated:
        is_admin = OrganizationMember.objects.filter(
            user=request.user,
            is_admin=True
        ).exists()
        return {"user_is_org_admin": is_admin}

    return {"user_is_org_admin": False}
