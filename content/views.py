from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import (
    Topic,
    Series,
    Teaching,
    BibleBook,
    Church,
    ChurchUpdate,
)

from .models import Church
from django.views.generic import ListView

def contact(request):
    return render(
        request,
        "content/contact.html",
    )
from .models import Church
def church_detail(request, pk):
    church = get_object_or_404(
        Church,
        pk=pk,
        is_active=True,
    )

    return render(
        request,
        "content/church_detail.html",
        {
            "church": church,
        },
    )
def church_list(request):
    churches = Church.objects.filter(
        is_active=True
    )

    churches_count = churches.count()

    countries_count = churches.values(
        "country"
    ).distinct().count()

    latest_church = churches.order_by(
        "-created_at"
    ).first()

    return render(request, "content/church_list.html", {
        "churches": churches,
        "churches_count": churches_count,
        "countries_count": countries_count,
        "latest_church": latest_church,
    })
def biblebook_list(request):

    old_testament = BibleBook.objects.filter(
        testament="OT"
    ).order_by("order")

    new_testament = BibleBook.objects.filter(
        testament="NT"
    ).order_by("order")

    return render(
        request,
        "content/biblebook_list.html",
        {
            "old_testament": old_testament,
            "new_testament": new_testament,
        },
    )
def biblebook_detail(request, pk):

    bible_book = get_object_or_404(BibleBook, pk=pk)

    teachings = bible_book.teachings.filter(
        is_published=True
    ).order_by("-published_at")

    return render(
        request,
        "content/biblebook_detail.html",
        {
            "bible_book": bible_book,
            "teachings": teachings,
        },
    )


def home(request):

    teachings = (
        Teaching.objects
        .filter(is_published=True)
        .order_by("-published_at")
    )

    churches = Church.objects.order_by("-id")

    church_updates = (
        ChurchUpdate.objects
        .filter(is_published=True)
        .select_related("church")
        .order_by("-date")
    )
    print("HOME UPDATES:", list(church_updates.values(
    "id",
    "title",
    "is_published",
)))

    context = {
        # Latest items
        "latest_teaching": teachings.first(),
        "latest_church": churches.first(),

        # Church updates
        "latest_updates": church_updates[:3],

        # Recent items
        "teachings": teachings[:5],
        "churches": churches[:5],

        # Lists
        "topics": Topic.objects.all(),

        # Statistics
        "teachings_count": teachings.count(),
        "topics_count": Topic.objects.count(),
        "churches_count": churches.count(),
        "series_count": Series.objects.count(),
    }

    return render(
        request,
        "content/home.html",
        context,
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
from .models import Teaching

def teaching_list(request):

    q = request.GET.get("q", "").strip()

    teachings = Teaching.objects.filter(
        is_published=True
    ).order_by("title")

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