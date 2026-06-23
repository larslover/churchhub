from django.shortcuts import render
from .models import Teaching, Topic, Series


def home(request):
    context = {
        "featured_teachings": Teaching.objects.filter(
            is_published=True
        )[:4],

        "recent_teachings": Teaching.objects.filter(
            is_published=True
        ).order_by("-published_at")[:10],

        "topics": Topic.objects.all(),

        "series": Series.objects.all()[:6],
    }

    return render(request, "home.html", context)