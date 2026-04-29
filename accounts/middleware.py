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