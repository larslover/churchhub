# content/views.py
from django.shortcuts import render
from .models import Update, Program, Media, Devotional

def devotional_archive(request):
    from .models import Devotional

    devotionals = Devotional.objects.all().order_by("-date")

    return render(
        request,
        "content/devotional_archive.html",
        {
            "devotionals": devotionals
        }
    )
from django.shortcuts import render
from .models import Update, Program, Media, Devotional 
from accounts.models import OrganizationMember




def home(request):
    membership = OrganizationMember.objects.filter(
        user=request.user,
        is_active=True
    ).select_related("organization").first()

    if not membership:
        return render(request, "home.html", {
            "programs": [],
            "media_items": [],
            "latest_update": None,
            "devotional": None,
            "organization": None,
        })

    organization = membership.organization

    programs = Program.objects.filter(
        is_active=True,
        organization=organization
    )

    media_items = Media.objects.filter(
        is_published=True,
        organization=organization
    )

    # Update model (assumes created_at exists)
    latest_update = Update.objects.filter(
        organization=organization
    ).order_by("-created_at").first()

    # Devotional model (uses 'date' NOT created_at)
    devotional = Devotional.objects.filter(
        is_active=True,
        organization=organization
    ).order_by("-date").first()

    return render(request, "home.html", {
        "programs": programs,
        "media_items": media_items,
        "latest_update": latest_update,
        "devotional": devotional,
        "organization": organization,
    })