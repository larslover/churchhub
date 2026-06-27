from django.shortcuts import render, get_object_or_404
from .models import Topic, Series, Teaching


def home(request):
    teachings = Teaching.objects.filter(
        is_published=True
    ).order_by("-published_at")

    return render(
        request,
        "content/home.html",
        {
            "teachings": teachings
        }
    )


def topic_list(request):
    topics = Topic.objects.all()

    return render(
        request,
        "content/topic_list.html",
        {
            "topics": topics
        }
    )


def topic_detail(request, slug):
    topic = get_object_or_404(Topic, slug=slug)

    teachings = topic.teachings.filter(
        is_published=True
    ).order_by("-published_at")

    return render(
        request,
        "content/topic_detail.html",
        {
            "topic": topic,
            "teachings": teachings,
        }
    )


def series_list(request):
    series = Series.objects.all()

    return render(
        request,
        "content/series_list.html",
        {
            "series": series
        }
    )