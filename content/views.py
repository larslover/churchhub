# content/views.py
from django.shortcuts import render
from .models import Update, Program, Media

def home(request):
    programs = Program.objects.filter(is_active=True)
    latest_update = Update.objects.filter(is_published=True).order_by("-created_at").first()
    media_items = Media.objects.filter(is_published=True)  # <-- use is_published, not is_active

    context = {
        "programs": programs,
        "latest_update": latest_update,
        "media_items": media_items,
    }
    return render(request, "home.html", context)