# =========================
# IMPORTS
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import base64
import qrcode
import io

from accounts.models import (
    OrganizationMember,
    OrganizationJoinRequest,
)

from engagement.models import Group
from content.models import Devotional,Update, Program

from .utils import get_admin_org


# =========================
# DASHBOARD
# =========================
@login_required
def org_dashboard_view(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    total_members = OrganizationMember.objects.filter(
        organization=org
    ).count()

    pending_requests = OrganizationJoinRequest.objects.filter(
        organization=org
    ).count()

    total_groups = Group.objects.filter(
        organization=org,
        is_active=True
    ).count()

    join_link = request.build_absolute_uri(
        f"/accounts/join/{org.join_code}/"
    )

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


# =========================
# REQUESTS
# =========================
@login_required
def org_requests_view(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    requests = OrganizationJoinRequest.objects.filter(
        organization=org
    ).select_related("user")

    return render(request, "org_admin/requests.html", {
        "requests": requests
    })

@login_required
def approve_org_request_view(request, request_id):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    # 🔐 tenant-safe fetch (IMPORTANT CHANGE)
    join_request = get_object_or_404(
        OrganizationJoinRequest,
        id=request_id,
        organization=org
    )

    OrganizationMember.objects.get_or_create(
        user=join_request.user,
        organization=org,
        defaults={
            "is_admin": False,
            "is_active": True
        }
    )

    join_request.delete()

    return redirect("org_admin:org_requests")
# =========================
# DEVOTIONALS
# =========================
@login_required
def devotional_list(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    devotionals = Devotional.objects.filter(
        organization=org
    ).order_by("-date")

    return render(request, "org_admin/devotionals.html", {
        "devotionals": devotionals
    })


# =========================
# PLACEHOLDERS
# =========================
@login_required
def update_list(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    updates = Update.objects.filter(
        organization=org
    )

    return render(request, "org_admin/updates.html", {
        "updates": updates
    })
    return render(request, "org_admin/updates.html")
@login_required
def update_create(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    if request.method == "POST":
        Update.objects.create(
            organization=org,
            title=request.POST.get("title"),
            body=request.POST.get("body"),
            image=request.FILES.get("image"),
            is_published=True
        )

        return redirect("org_admin:update_list")

    return render(request, "org_admin/update_form.html")

@login_required
def update_edit(request, pk):
    org = get_admin_org(request)

    update = get_object_or_404(
        Update,
        pk=pk,
        organization=org
    )

    if request.method == "POST":
        update.title = request.POST.get("title")
        update.body = request.POST.get("body")

        if request.FILES.get("image"):
            update.image = request.FILES.get("image")

        update.save()

        return redirect("org_admin:update_list")

    return render(request, "org_admin/update_form.html", {
        "update": update
    })
@login_required
def update_delete(request, pk):
    org = get_admin_org(request)

    update = get_object_or_404(
        Update,
        pk=pk,
        organization=org
    )

    if request.method == "POST":
        update.delete()
        return redirect("org_admin:update_list")

    return render(request, "org_admin/update_delete.html", {
        "update": update
    })
from content.models import Media


@login_required
def media_list(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    items = Media.objects.filter(
        organization=org
    ).order_by("-created_at")

    return render(request, "org_admin/media.html", {
        "items": items
    })


@login_required
def media_create(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    if request.method == "POST":
        Media.objects.create(
            organization=org,
            title=request.POST.get("title"),
            media_type=request.POST.get("media_type"),
            media_url=request.POST.get("media_url"),
            is_published=True
        )

        return redirect("org_admin:media_list")

    return render(request, "org_admin/media_form.html")


@login_required
def media_edit(request, pk):
    org = get_admin_org(request)

    media = get_object_or_404(
        Media,
        pk=pk,
        organization=org
    )

    if request.method == "POST":
        media.title = request.POST.get("title")
        media.media_type = request.POST.get("media_type")
        media.media_url = request.POST.get("media_url")
        media.save()

        return redirect("org_admin:media_list")

    return render(request, "org_admin/media_form.html", {
        "media": media
    })


@login_required
def media_delete(request, pk):
    org = get_admin_org(request)

    media = get_object_or_404(
        Media,
        pk=pk,
        organization=org
    )

    if request.method == "POST":
        media.delete()
        return redirect("org_admin:media_list")

    return render(request, "org_admin/media_delete.html", {
        "media": media
    })
@login_required
def program_list(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    programs = Program.objects.filter(
        organization=org
    ).order_by("-created_at")

    return render(request, "org_admin/programs.html", {
        "programs": programs
    })
@login_required
def program_create(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    if request.method == "POST":
        Program.objects.create(
            organization=org,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            image=request.FILES.get("image"),
            day=request.POST.get("day"),
            time=request.POST.get("time"),
            is_active=True
        )

        return redirect("org_admin:program_list")

    return render(request, "org_admin/program_form.html")
@login_required
def program_edit(request, pk):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    program = get_object_or_404(
        Program,
        pk=pk,
        organization=org   # 🔐 critical SaaS protection
    )

    if request.method == "POST":
        program.title = request.POST.get("title")
        program.description = request.POST.get("description")
        program.day = request.POST.get("day")
        program.time = request.POST.get("time")

        if request.FILES.get("image"):
            program.image = request.FILES.get("image")

        program.save()

        return redirect("org_admin:program_list")

    return render(request, "org_admin/program_form.html", {
        "program": program
    })

@login_required
def program_delete(request, pk):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    program = get_object_or_404(
        Program,
        pk=pk,
        organization=org  # 🔐 prevents cross-org deletion
    )

    if request.method == "POST":
        program.delete()
        return redirect("org_admin:program_list")

    return render(request, "org_admin/program_delete.html", {
        "program": program
    })


@login_required
def devotional_create(request):
    org = get_admin_org(request)

    if not org:
        return redirect("home")

    if request.method == "POST":
        Devotional.objects.create(
            organization=org,
            title=request.POST.get("title"),
            verse_reference=request.POST.get("verse_reference"),
            verse_text=request.POST.get("verse_text"),
            message=request.POST.get("message"),
            is_active=True
        )

        messages.success(request, "Devotional created.")
        return redirect("org_admin:devotional_list")

    return render(request, "org_admin/devotional_form.html")
@login_required
def devotional_edit(request, pk):
    org = get_admin_org(request)

    devotional = get_object_or_404(
        Devotional,
        pk=pk,
        organization=org
    )

    if request.method == "POST":
        devotional.title = request.POST.get("title")
        devotional.verse_reference = request.POST.get("verse_reference")
        devotional.verse_text = request.POST.get("verse_text")
        devotional.message = request.POST.get("message")
        devotional.save()

        return redirect("org_admin:devotional_list")

    return render(request, "org_admin/devotional_form.html", {
        "devotional": devotional
    })
@login_required
def devotional_delete(request, pk):
    org = get_admin_org(request)

    devotional = get_object_or_404(
        Devotional,
        pk=pk,
        organization=org
    )

    if request.method == "POST":
        devotional.delete()
        return redirect("org_admin:devotional_list")

    return render(request, "org_admin/devotional_delete.html", {
        "devotional": devotional
    })