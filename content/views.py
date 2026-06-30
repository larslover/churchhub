from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Topic, Series, Teaching


def home(request):
    teachings = Teaching.objects.filter(
        is_published=True
    ).order_by("-published_at")

    latest_teaching = teachings.first()
    recent_teachings = teachings[:5]

    return render(request, "content/home.html", {
        "latest_teaching": latest_teaching,
        "teachings": recent_teachings,
        "topics": Topic.objects.all(),

        # (optional but needed for stats if you use them)
        "teachings_count": teachings.count(),
        "topics_count": Topic.objects.count(),
        "series_count": Series.objects.count(),
    })
def topic_list(request):
    topics = Topic.objects.all()

    return render(
        request,
        "content/topic_list.html",
        {
            "topics": topics
        }
    )
from .models import Teaching

def teaching_list(request):

    q = request.GET.get("q", "").strip()

    teachings = Teaching.objects.filter(
        is_published=True
    ).order_by("-published_at")

    if q:
        teachings = teachings.filter(
            Q(title__icontains=q) |
            Q(summary__icontains=q) |
            Q(content__icontains=q)
        )

    return render(request, "content/teaching_list.html", {
        "teachings": teachings,
        "q": q,
    })
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)

    teachings = topic.teachings.filter(
        is_published=True
    ).order_by("-published_at")

    return render(request, "content/topic_detail.html", {
        "topic": topic,
        "teachings": teachings,
    })

def teaching_detail(request, pk):
    teaching = get_object_or_404(Teaching, pk=pk)
    return render(request, "content/teaching_detail.html", {
        "teaching": teaching
    })

def series_list(request):
    series = Series.objects.all()

    return render(
        request,
        "content/series_list.html",
        {
            "series": series
        }
    )