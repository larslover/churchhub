# =========================
# IMPORTS (CLEANED)
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import io
import base64
import qrcode

from .models import (
    Organization,
    OrganizationMember,
    OrganizationJoinRequest,
)

from engagement.models import Group
from .forms import CustomUserCreationForm
from .phone_utils import COUNTRY_CODES


# =========================
# HELPERS
# =========================
def set_active_org(request, org_id):
    request.session["organization_id"] = org_id


def get_active_org(request):
    org_id = request.session.get("organization_id")
    if not org_id:
        return None
    return Organization.objects.filter(id=org_id).first()


# =========================
# SIGNUP
# =========================
def signup_view(request):
    print("sign up view triggered")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            pending_code = request.session.get("pending_org_code")

            if pending_code:
                return redirect(f"/accounts/join/{pending_code}/")

            return redirect("connect_organization")

        print(form.errors)  # 🔥 DEBUG
        print(request.POST)
        

    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {
        "form": form,
        "country_codes": COUNTRY_CODES
    })
# =========================
# LOGIN (FIXED SaaS FLOW)
# =========================
def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()
        password = request.POST.get("password", "")
        country_code = request.POST.get("country_code", "").strip()

        if "@" not in identifier:
            identifier = identifier.replace(" ", "").replace("-", "")
            if country_code:
                identifier = f"{country_code}{identifier}"

        user = authenticate(request, username=identifier, password=password)

        if user:
            login(request, user)

            memberships = OrganizationMember.objects.filter(
                user=user,
                is_active=True
            ).select_related("organization")

            if not memberships.exists():
                request.session.pop("organization_id", None)
                return redirect("connect_organization")

            # ALWAYS set default org (prevents UI break)
            org = memberships.first().organization
            set_active_org(request, org.id)

            if memberships.count() > 1:
                return redirect("select_organization")

            return redirect("home")

        messages.error(request, "Invalid login credentials.")

    return render(request, "registration/login.html", {
        "country_codes": COUNTRY_CODES
    })


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect("login")


# =========================
# CREATE ORGANIZATION
# =========================
from .phone_utils import COUNTRY_CODES
def organization_signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            org_name = request.POST.get("org_name", "").strip()
            slug = request.POST.get("slug", "").strip()

            organization = Organization.objects.create(
                name=org_name,
                slug=slug
            )

            user = form.save()

            OrganizationMember.objects.create(
                user=user,
                organization=organization,
                is_admin=True
            )

            login(request, user)
            request.session["organization_id"] = organization.id

            return redirect("home")

        return render(request, "registration/org_signup.html", {
            "form_errors": form.errors,
            "country_codes": COUNTRY_CODES
        })

    return render(request, "registration/org_signup.html", {
        "country_codes": COUNTRY_CODES
    })# =========================
# JOIN ORGANIZATION (SINGLE FLOW)
# =========================
def join_organization_view(request, code):
    organization = get_object_or_404(
        Organization,
        join_code=code,
        is_active=True
    )

    if not request.user.is_authenticated:
        request.session["pending_org_code"] = code
        return redirect(f"/accounts/login/?next=/accounts/join/{code}/")

    # already member → switch org
    if OrganizationMember.objects.filter(
        user=request.user,
        organization=organization
    ).exists():
        set_active_org(request, organization.id)
        return redirect("home")

    # request join
    OrganizationJoinRequest.objects.get_or_create(
        user=request.user,
        organization=organization
    )

    messages.success(request, "Join request sent.")
    return redirect("home")


# =========================
# CONNECT BY CODE (manual fallback)
# =========================
@login_required
def connect_organization_view(request):
    if request.method == "POST":
        code = request.POST.get("invite_code", "").strip().upper()

        organization = get_object_or_404(Organization, join_code=code, is_active=True)

        OrganizationMember.objects.get_or_create(
            user=request.user,
            organization=organization,
            defaults={"is_admin": False, "is_active": True}
        )

        set_active_org(request, organization.id)

        return redirect("home")

    return render(request, "registration/connect_organization.html")


# =========================
# FIND CHURCH
# =========================
@login_required
def find_church_view(request):
    query = request.GET.get("q", "").strip()

    orgs = Organization.objects.filter(is_active=True)

    if query:
        orgs = orgs.filter(Q(name__icontains=query) | Q(slug__icontains=query))

    return render(request, "registration/find_church.html", {
        "organizations": orgs[:20],
        "query": query
    })


# =========================
# ADMIN REQUESTS
# =========================

# =========================
# APPROVE REQUEST
# =========================

# =========================
# DASHBOARD
# =========================


# =========================
# REGENERATE CODE
# =========================
@login_required
def regenerate_join_code_view(request):
    membership = OrganizationMember.objects.filter(
        user=request.user,
        is_admin=True
    ).select_related("organization").first()

    if not membership:
        return redirect("home")

    org = membership.organization
    org.join_code = org.generate_join_code()
    org.save()

    return redirect("org_dashboard")
def terms(request):
    return render(request, "legal/terms.html")


def privacy(request):
    return render(request, "legal/privacy.html")

@login_required
def approve_org(request, request_id):
    if not request.user.is_superuser:
        return redirect("home")

    req = get_object_or_404(OrganizationJoinRequest, id=request_id)

    org = req.organization
    creator = req.user   # or req.user depending on your intent

    if request.method == "POST":
        org.is_active = True
        org.save()

        OrganizationMember.objects.get_or_create(
            user=creator,
            organization=org,
            defaults={"is_admin": True, "is_active": True}
        )

        req.approved = True
        req.save()

    return redirect("admin_org_requests")