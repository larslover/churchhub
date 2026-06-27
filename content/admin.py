from django.contrib import admin
from .models import Topic, Series, Tag, Teaching, Resource


@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "series",
        "is_published",
        "published_at",
    )

    list_filter = (
        "is_published",
        "topic",
        "series",
    )

    search_fields = (
        "title",
        "summary",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }


admin.site.register(Topic)
admin.site.register(Series)
admin.site.register(Tag)
admin.site.register(Resource)