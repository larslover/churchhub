# content/context_processors.py

from .models import Update

def global_updates(request):
    """
    Provides all published updates for a site-wide banner or sidebar
    """
    updates = Update.objects.filter(is_published=True).order_by("-created_at")
    return {"global_updates": updates}


