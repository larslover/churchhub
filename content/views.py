from django.shortcuts import render
from .models import Teaching


def home(request):

    latest_teachings = (
        Teaching.objects
        .filter(is_published=True)
        .order_by("-published_at")[:10]
    )

    return render(
        request,
        "home.html",
        {
            "latest_teachings": latest_teachings,
        }
    )