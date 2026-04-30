# =========================
# IMPORTS
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

import io
import base64
import qrcode

from accounts.models import (
    Organization,
    OrganizationMember,
    OrganizationJoinRequest,
)

from engagement.models import Group  # adjust if your app name differs
@login_required
def org_requests_view(request):
    membership = OrganizationMember.objects.filter(
        user=request.user,
        is_admin=True
    ).select_related("organization").first()

    if not membership:
        return redirect("home")

    requests = OrganizationJoinRequest.objects.filter(
        organization=membership.organization
    ).select_related("user")

    return render(request, "accounts/org_requests.html", {
        "requests": requests
    })


# =========================
# APPROVE JOIN REQUEST
# =========================
@login_required
def approve_org_request_view(request, request_id):
    join_request = get_object_or_404(OrganizationJoinRequest, id=request_id)

    is_admin = OrganizationMember.objects.filter(
        user=request.user,
        organization=join_request.organization,
        is_admin=True
    ).exists()

    if not is_admin:
        return redirect("home")

    OrganizationMember.objects.create(
        user=join_request.user,
        organization=join_request.organization,
        is_admin=False,
        is_active=True
    )

    join_request.delete()

    return redirect("org_requests")


# =========================
# ORG DASHBOARD
# =========================
@login_required
def org_dashboard_view(request):
    membership = OrganizationMember.objects.filter(
        user=request.user,
        is_admin=True
    ).select_related("organization").first()

    if not membership:
        return redirect("home")

    org = membership.organization

    total_members = OrganizationMember.objects.filter(organization=org).count()
    pending_requests = OrganizationJoinRequest.objects.filter(organization=org).count()
    total_groups = Group.objects.filter(organization=org, is_active=True).count()

    join_link = request.build_absolute_uri(f"/accounts/join/{org.join_code}/")

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(join_link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "org_admin/dashboard.html", {
        "organization": org,
        "total_members": total_members,
        "pending_requests": pending_requests,
        "total_groups": total_groups,
        "join_link": join_link,
        "qr_code": qr_code,
    })