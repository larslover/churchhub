# content/views.py
from django.shortcuts import render
from .models import Update, Program, Media, Devotional

def devotional_archive(request):
    from .models import Devotional
    devotionals = Devotional.objects.filter(is_active=True)

    return render(request, "content/devotional_archive.html", {"devotionals": devotionals})

def home(request):
    programs = Program.objects.filter(is_active=True)
    latest_update = Update.objects.filter(is_published=True)\
                                  .order_by("-created_at")\
                                  .first()

    media_items = Media.objects.filter(is_published=True)

    # 🔥 Get latest active devotional
    devotional = Devotional.objects.filter(is_active=True)\
                                    .order_by("-date")\
                                    .first()

    context = {
        "programs": programs,
        "latest_update": latest_update,
        "media_items": media_items,
        "devotional": devotional,  # ← add this
    }

    return render(request, "home.html", context)