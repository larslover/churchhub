from accounts.models import Organization
from django.shortcuts import redirect
from accounts.models import Organization

class OrganizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        org_id = request.session.get("organization_id")
        request.organization = None

        if org_id:
            request.organization = Organization.objects.filter(id=org_id).first()

        return self.get_response(request)
    
class OrganizationRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # allow public pages
        allowed_paths = [
        "/accounts/login/",
        "/accounts/signup/",
        "/accounts/join/",
            "/accounts/connect/",
        ]

        if any(request.path.startswith(path) for path in allowed_paths):
            return self.get_response(request)

        # only enforce if logged in
        if user.is_authenticated:
            org_id = request.session.get("organization_id")

            if not org_id:
                return redirect("connect_organization")

        return self.get_response(request)