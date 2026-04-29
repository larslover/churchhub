from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import CustomUserCreationForm
from .phone_utils import COUNTRY_CODES

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .models import Organization, OrganizationMember,OrganizationJoinRequest
from .forms import CustomUserCreationForm
# ===============================
# 📝 SIGNUP
# ===============================
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Organization, OrganizationMember


@login_required
def connect_organization_view(request):
    if request.method == "POST":
        invite_code = request.POST.get("invite_code", "").strip().upper()

        try:
            organization = Organization.objects.get(
                join_code=invite_code,
                is_active=True
            )

            # Create membership
            OrganizationMember.objects.get_or_create(
                user=request.user,
                organization=organization,
                defaults={
                    "is_admin": False,
                    "is_active": True
                }
            )

            # Set active org
            request.session["organization_id"] = organization.id

            messages.success(
                request,
                f"You joined {organization.name} successfully."
            )

            return redirect("home")

        except Organization.DoesNotExist:
            messages.error(request, "Invalid church code.")

    return render(request, "registration/connect_organization.html")
def signup_view(request):
    if request.method == "POST":
        post_data = request.POST.copy()

        country_code = post_data.get("country_code", "").strip()
        local_phone = (
            post_data.get("local_phone", "")
            .strip()
            .replace(" ", "")
            .replace("-", "")
        )

        # Combine full phone number
        post_data["phone"] = f"{country_code}{local_phone}"

        form = CustomUserCreationForm(post_data)

        if form.is_valid():
            user = form.save()

            # Log user in
            login(request, user)

            messages.success(
                request,
                "Account created successfully. Now connect to your church."
            )

            # 🔥 IMPORTANT CHANGE
            return redirect("connect_organization")

        else:
            print(form.errors)

    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {
        "form": form
    })
# ===============================
# 🔐 LOGIN
# ===============================
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import OrganizationMember
from .phone_utils import COUNTRY_CODES
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

        if user is not None:
            login(request, user)

            memberships = OrganizationMember.objects.filter(
                user=user,
                is_active=True,
                organization__isnull=False
            ).select_related("organization")

            if memberships.count() == 1:
                request.session["organization_id"] = memberships.first().organization_id
                return redirect("home")

            elif memberships.exists():
                return redirect("select_organization")

            else:
                request.session.pop("organization_id", None)
                messages.error(request, "No organization assigned to this account.")
                return redirect("login")

        messages.error(request, "Invalid login credentials.")

    return render(request, "registration/login.html", {
        "country_codes": COUNTRY_CODES
    })
# 🚪 LOGOUT
# ===============================
def logout_view(request):
    logout(request)
    return redirect("login")
def organization_signup_view(request):
    if request.method == "POST":

        org_name = request.POST.get("org_name", "").strip()
        slug = request.POST.get("slug", "").strip()

        country_code = request.POST.get("country_code", "").strip()
        local_phone = request.POST.get("local_phone", "").strip().replace(" ", "").replace("-", "")
        phone = f"{country_code}{local_phone}"

        password = request.POST.get("password")
        full_name = request.POST.get("full_name")

        form = CustomUserCreationForm({
            "phone": phone,
            "full_name": full_name,
            "password1": password,
            "password2": password
        })

        if not form.is_valid():
            return render(request, "registration/org_signup.html", {"form_errors": form.errors})

        # 1. create org
        organization = Organization.objects.create(
            name=org_name,
            slug=slug
        )

        # 2. create user
        user = form.save()

        # 3. link user to org
        OrganizationMember.objects.create(
            user=user,
            organization=organization,
            is_admin=True
        )

        # 4. login
        login(request, user)

        # 5. set session
        request.session["organization_id"] = organization.id

        messages.success(request, "Organization created successfully.")
        return redirect("home")

    return render(request, "registration/org_signup.html")

from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def find_church_view(request):
    query = request.GET.get("q", "").strip()

    organizations = Organization.objects.filter(is_active=True)

    if query:
        organizations = organizations.filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query)
        )

    return render(request, "registration/find_church.html", {
        "organizations": organizations[:20],
        "query": query
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import (
    Organization,
    OrganizationMember,
    OrganizationJoinRequest,
)


# ==================================
# USER REQUESTS ACCESS TO CHURCH
# ==================================
@login_required
def request_org_access_view(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)

    OrganizationJoinRequest.objects.get_or_create(
        user=request.user,
        organization=organization
    )

    messages.success(
        request,
        f"Access request sent to {organization.name}."
    )

    return redirect("find_church")


# ==================================
# ADMIN SEES PENDING REQUESTS
# ==================================
@login_required
def org_requests_view(request):
    membership = OrganizationMember.objects.filter(
        user=request.user,
        is_admin=True
    ).first()

    if not membership:
        messages.error(request, "Admins only.")
        return redirect("home")

    requests = OrganizationJoinRequest.objects.filter(
        organization=membership.organization
    ).select_related("user")

    return render(request, "accounts/org_requests.html", {
        "requests": requests
    })


# ==================================
# ADMIN APPROVES REQUEST
# ==================================
@login_required
def approve_org_request_view(request, request_id):
    join_request = get_object_or_404(
        OrganizationJoinRequest,
        id=request_id
    )

    is_admin = OrganizationMember.objects.filter(
        user=request.user,
        organization=join_request.organization,
        is_admin=True
    ).exists()

    if not is_admin:
        messages.error(request, "Admins only.")
        return redirect("home")

    OrganizationMember.objects.get_or_create(
        user=join_request.user,
        organization=join_request.organization,
        defaults={"is_admin": False}
    )

    join_request.delete()

    messages.success(request, "Member approved.")
    return redirect("org_requests")

@login_required
def org_dashboard_view(request):
    membership = OrganizationMember.objects.filter(
        user=request.user,
        is_admin=True
    ).select_related("organization").first()

    if not membership:
        messages.error(request, "Admins only.")
        return redirect("home")

    organization = membership.organization

    total_members = OrganizationMember.objects.filter(
        organization=organization
    ).count()

    pending_requests = OrganizationJoinRequest.objects.filter(
        organization=organization
    ).count()

    return render(request, "org_dashboard.html", {
        "organization": organization,
        "total_members": total_members,
        "pending_requests": pending_requests,
    })